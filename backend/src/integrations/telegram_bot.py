import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from src.config import settings
from src.db.database import SessionLocal
from src.services.orchestrator import process_query

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Welcome to IntelliKnow KMS!\n\n"
        "Ask me anything about your company's knowledge base.\n"
        "For example: 'What is the annual leave policy?'"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    query = update.message.text.strip()
    user_id = str(update.effective_user.id) if update.effective_user else None

    await update.message.chat.send_action("typing")

    db = SessionLocal()
    try:
        result = process_query(query, "telegram", user_id, db)
        await update.message.reply_text(result.channel_formatted)
    except Exception as exc:
        logger.error("Error processing Telegram message: %s", exc)
        await update.message.reply_text("Sorry, I encountered an error. Please try again.")
    finally:
        db.close()


def build_telegram_app() -> Application | None:
    token = settings.telegram_bot_token
    if not token:
        logger.warning("TELEGRAM_BOT_TOKEN not set — Telegram integration disabled")
        return None

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return app


def run_polling() -> None:
    """Run Telegram bot in polling mode (blocking). Called in a background thread."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = build_telegram_app()
    if app:
        logger.info("Starting Telegram bot in polling mode...")
        app.run_polling(drop_pending_updates=True)
