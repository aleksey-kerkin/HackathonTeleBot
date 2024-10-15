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
        rf"Привет {user.mention_html()}! Этот бот создан для планирования отпусков. Что хочешь сделать?",
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
            [[InlineKeyboardButton("Отмена", callback_data=f"cancel_plan_{chat_id}")]]
        ),
    )
    context.user_data["waiting_for_date"] = True


async def confirm_plan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    message_text = update.message.text.strip()

    if context.user_data.get("waiting_for_date"):
        try:
            start_date = datetime.strptime(message_text, "%Y-%m-%d")
            end_date = start_date + timedelta(days=14)
            end_date_str = end_date.strftime("%Y-%m-%d")

            vacation_info = {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date_str,
                "is_approved": False,
                "tickets_booked": False,
            }

            save_vacation(chat_id, vacation_info)

            await update.message.reply_text(
                f"Отпуск запланирован:\n"
                f"Начало: {start_date.strftime('%Y-%m-%d')}\n"
                f"Конец: {end_date_str}"
            )
            context.user_data["waiting_for_date"] = False
        except ValueError:
            await update.message.reply_text(
                "Неверный формат даты. Пожалуйста, используйте формат YYYY-MM-DD."
            )
    else:
        await update.message.reply_text(
            "Пожалуйста, сначала нажмите 'Запланировать отпуск'."
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
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(vacation_text)
    else:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            "У вас нет запланированных отпусков."
        )
