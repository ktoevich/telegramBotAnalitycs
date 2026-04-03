import os
import google.generativeai as genai

async def summarize_lesson(messages: list) -> str:
    """Takes a list of message tuples (username, text, timestamp) and returns a summary."""
    if not messages:
        return "Нет сообщений для данного урока."

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Ошибка: не задан ключ GEMINI_API_KEY."

    genai.configure(api_key=api_key)
    # Using 'gemini-flash-latest' based on available models
    model = genai.GenerativeModel('gemini-flash-latest')

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

    try:
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        return f"Произошла ошибка при генерации ответа от AI: {e}"
