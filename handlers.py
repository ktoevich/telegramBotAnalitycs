import datetime
from aiogram import Router, F, types
from aiogram.filters import Command

import db
import llm

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот для резюмирования уроков. \n"
                         "Добавьте меня в группу, и я буду записывать сообщения, чтобы потом сделать выжимку обсуждения. \n"
                         "Используйте команду /summary, чтобы получить конспект сегодняшнего урока, "
                         "или /summary YYYY-MM-DD для конкретной даты.")

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Команды:\n"
                         "/start - Приветствие\n"
                         "/help - Справка\n"
                         "/summary [YYYY-MM-DD] - Получить краткий конспект урока (по умолчанию за сегодня).")

@router.message(Command("summary"))
async def cmd_summary(message: types.Message, command: Command):
    # Determine the date
    args = command.args
    if args:
        try:
            # Validate simple date format YYYY-MM-DD
            datetime.datetime.strptime(args.strip(), "%Y-%m-%d")
            lesson_date = args.strip()
        except ValueError:
            await message.reply("Неверный формат даты. Пожалуйста, используйте формат YYYY-MM-DD, например 2024-05-12.")
            return
    else:
        lesson_date = datetime.date.today().isoformat()

    chat_id = message.chat.id
    
    # Let the chat know the bot is thinking
    status_msg = await message.reply(f"Собираю сообщения за {lesson_date} и готовлю результат...")

    messages = db.get_messages(chat_id, lesson_date)
    
    if not messages:
        await status_msg.edit_text(f"Не нашел сообщений за урок от {lesson_date}.")
        return

    # Generate summary using LLM
    summary = await llm.summarize_lesson(messages)

    # Telegram message maximum length is 4096 characters.
    # In case summary is very long, it should ideally be chunked, 
    # but for typical summaries, it fits well.
    import html
    if len(summary) > 4050:
        summary = summary[:4050] + "...\n[Обрезано]"

    safe_summary = html.escape(summary)
    text = f"🎓 <b>Конспект урока ({lesson_date})</b>\n\n{safe_summary}"
    await status_msg.edit_text(text, parse_mode="HTML")

# Message handler must be at the bottom to catch all text messages
@router.message(F.text & ~F.text.startswith('/'))
async def handle_text_message(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name or "Unknown"
    text = message.text
    lesson_date = datetime.date.today().isoformat()

    # Save to db
    db.add_message(chat_id, user_id, username, text, lesson_date)
