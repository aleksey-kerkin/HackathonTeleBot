import logging
from datetime import datetime, timedelta

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from database import create_table, get_vacations, save_vacation

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Этот бот создан для планирования отпусков. Что хочешь сделать?",  # noqa: E501
    )
    keyboard = [
        [
            InlineKeyboardButton("Запланировать отпуск", callback_data="plan_vacation"),
            InlineKeyboardButton(
                "Посмотреть запланированное", callback_data="get_vacations"
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)


async def plan_vacation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    existing_vacations = get_vacations(chat_id)

    if existing_vacations:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            "У вас уже есть запланированные отпуска."
        )
        return

    create_table()

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Введите дату начала отпуска (YYYY-MM-DD):",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Закрепить", callback_data=f"confirm_plan_{chat_id}"
                    ),
                    InlineKeyboardButton(
                        "Отмена", callback_data=f"cancel_plan_{chat_id}"
                    ),
                ]
            ]
        ),
    )


async def confirm_plan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    query = update.callback_query

    message_text = query.message.text
    start_date = message_text.strip()

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = start_date + timedelta(days=14)
        end_date_str = end_date.strftime("%Y-%m-%d")

        vacation_info = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date_str,
            "is_approved": False,
            "tickets_booked": False,
        }

        save_vacation(chat_id, vacation_info)

        await query.answer()
        await query.edit_message_text(
            f"Отпуск запланирован:\n"
            f"Начало: {start_date.strftime('%Y-%m-%d')}\n"
            f"Конец: {end_date_str}"
        )
    except ValueError:
        await query.answer()
        await query.edit_message_text(
            "Неверный формат даты. Пожалуйста, используйте формат YYYY-MM-DD."
        )


async def view_planned(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    existing_vacations = get_vacations(chat_id)

    if existing_vacations:
        vacation_info = {
            "start_date": existing_vacations[2],
            "end_date": existing_vacations[3],
        }
        vacation_text = f"{vacation_info['start_date']} - {vacation_info['end_date']}"
        await update.message.reply_text(vacation_text)
    else:
        await update.message.reply_text("У вас нет запланированных отпусков.")
