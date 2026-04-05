import os
import google.generativeai as genai

async def summarize_lesson(messages: list) -> str:
    """Takes a list of message tuples (username, text, timestamp) and returns a summary."""
    if not messages:
        return "Нет сообщений для данного урока."

    keys_to_try = [os.getenv("GEMINI_API_KEY"), os.getenv("GEMINI_API_KEY_2")]
    keys_to_try = [k for k in keys_to_try if k]
    if not keys_to_try:
        return "Ошибка: не заданы ключи GEMINI_API_KEY."

    prompt = (
        "Пожалуйста, проанализируй следующий лог сообщений из чата урока.\n"
        "1. Определи главную тему, которая обсуждалась.\n"
        "2. Сделай краткую выжимку (summary) основных выводов и мнений участников.\n"
        "3. Структурируй ответ так, чтобы его было легко читать (маркированные списки, заголовки).\n"
        "4. Избегай упоминания конкретных имён, если это не принципиально, сосредоточься на самих идеях.\n\n"
        "Лог сообщений:\n"
    )

    for username, text, timestamp in messages:
        prompt += f"[{timestamp}] {username}: {text}\n"

    last_error = None
    for api_key in keys_to_try:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-flash-latest')
            response = await model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            last_error = e
            # Try the next API key if available
            continue

    return f"Произошла ошибка при генерации ответа от AI (все ключи не сработали): {last_error}"
