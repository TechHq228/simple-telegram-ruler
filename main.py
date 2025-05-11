from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DISCUSSION_CHAT_ID = int(os.getenv("DISCUSSION_CHAT_ID"))  # ID чата обсуждения
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # ID самого канала (не username!)

RULES_TEXT = """
📌 Правила чата:
1. Уважайте друг друга
2. Без рекламы и спама
3. Соблюдайте тему поста
"""

async def handle_forwarded_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message

    # Проверяем, что сообщение — переслано из нужного канала
    if message.forward_from_chat and message.forward_from_chat.id == CHANNEL_ID:
        try:
            await context.bot.send_message(
                chat_id=DISCUSSION_CHAT_ID,
                text=RULES_TEXT,
                reply_to_message_id=message.message_id
            )
            print(f"✅ Комментарий добавлен к дублированному сообщению {message.message_id}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Слушаем только сообщения в группе обсуждения
    discussion_handler = MessageHandler(
        filters.Chat(chat_id=DISCUSSION_CHAT_ID) & filters.FORWARDED,
        handle_forwarded_post
    )

    app.add_handler(discussion_handler)
    app.run_polling()

if __name__ == '__main__':
    main()
