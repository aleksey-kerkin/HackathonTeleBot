import logging

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import TOKEN
from vacation_planner import confirm_plan, plan_vacation, start, view_planned

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        CallbackQueryHandler(plan_vacation, pattern=r"^plan_vacation$")
    )
    application.add_handler(
        CallbackQueryHandler(view_planned, pattern=r"^get_vacations$")
    )
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_plan)
    )

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
