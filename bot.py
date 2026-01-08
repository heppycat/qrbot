import logging
import os
from io import BytesIO

import qrcode
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

BALE_BASE_URL = "https://tapi.bale.ai/bot"
BALE_FILE_URL = "https://tapi.bale.ai/file/bot"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = ReplyKeyboardMarkup(
        [["help"], ["start"]],
        resize_keyboard=True,
        one_time_keyboard=False,
    )
    await update.message.reply_text(
            "سلام! یه متن یا لینک برام بفرست تا به بارکد تبدیلش کنم.",
        reply_markup=keyboard,
    )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text(
        """یه متن بفرست تا برات به بارکد تبدیلش کنم!
پشتیبانی: @sleepi"""
        )
        return

    text = " ".join(context.args).strip()
    if not text:
        await update.message.reply_text(
        """یه متن بفرست تا برات به بارکد تبدیلش کنم!
پشتیبانی: @sleepi"""
        )
        return

    img = qrcode.make(text)
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    await update.message.reply_photo(photo=buf, caption="ایجاد شده با @qrcodesbot")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()
    command = text.lstrip("/").lower()
    if command == "start":
        await start(update, context)
        return
    if command == "help":
        await help(update, context)
        return

    if not text:
        await update.message.reply_text("یه متن بفرست تا برات به بارکد تبدیلش کنم!")
        return

    img = qrcode.make(text)
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    await update.message.reply_photo(photo=buf, caption="ایجاد شده با @qrcodesbot")


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        level=logging.INFO,
    )

    token = os.environ.get("BALE_BOT_TOKEN")
    if not token:
        raise SystemExit("Missing BALE_BOT_TOKEN env var.")

    app = (
        ApplicationBuilder()
        .token(token)
        .base_url(BALE_BASE_URL)
        .base_file_url(BALE_FILE_URL)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logging.info("Bale bot started. Waiting for updates...")
    app.run_polling()


if __name__ == "__main__":
    main()
