from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import TOKEN
from database import create_table
from handlers import error_handler, handle_callback, handle_text, plan, show, start


def main():
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler("start", start)
    plan_handler = CallbackQueryHandler(plan, pattern="^plan$")
    show_handler = CallbackQueryHandler(show, pattern="^show$")
    callback_handler = CallbackQueryHandler(handle_callback)
    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text)

    application.add_handler(start_handler)
    application.add_handler(plan_handler)
    application.add_handler(show_handler)
    application.add_handler(callback_handler)
    application.add_handler(text_handler)

    application.add_error_handler(error_handler)

    application.run_polling()


if __name__ == "__main__":
    create_table()
    main()
