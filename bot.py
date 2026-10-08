"""Telegram assistant: messaging layer.

The messaging layer is kept separate from the assistant logic (assistant.py),
so another channel (e.g. WhatsApp) can be added later as a second adapter.
"""

import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from assistant import handle_message

load_dotenv()

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("bot")

# Optional allow-list: comma-separated Telegram user IDs, e.g. "12345,67890".
# If empty, anyone who finds the bot can use it, so set this before going live.
ALLOWED_USERS = {
    int(uid) for uid in os.getenv("ALLOWED_USER_IDS", "").split(",") if uid.strip()
}


def is_allowed(update: Update) -> bool:
    if not ALLOWED_USERS:
        return True
    user = update.effective_user
    return user is not None and user.id in ALLOWED_USERS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    logger.info("/start from user id=%s", user.id if user else None)
    if not is_allowed(update):
        await update.message.reply_text("Sorry, you're not authorized to use this bot.")
        return
    await update.message.reply_text(
        f"Hi! Your Telegram user ID is {user.id}. Send me a message and I'll reply."
    )


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_allowed(update):
        await update.message.reply_text("Sorry, you're not authorized to use this bot.")
        return
    user_id = update.effective_user.id
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    reply = await handle_message(user_id, update.message.text)
    await update.message.reply_text(reply)


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Unhandled error", exc_info=context.error)


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("TELEGRAM_BOT_TOKEN is not set. See .env.example.")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.add_error_handler(on_error)

    logger.info("Bot started (polling)")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
