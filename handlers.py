from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from database import get_vacations, save_vacation


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Начать планирование", callback_data="plan")],
        [InlineKeyboardButton("Показать планы", callback_data="show")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Я бот-планер отпуска. Чтобы начать, выбери действие:",
        reply_markup=reply_markup,
    )


async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Да", callback_data="yes"),
            InlineKeyboardButton("Нет", callback_data="no"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "Согласовал ли ты даты своего отпуска с руководством?",
        reply_markup=reply_markup,
    )
    context.user_data["step"] = "is_approved"


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    data = query.data

    if context.user_data.get("step") == "is_approved":
        if data == "yes":
            context.user_data["vacation"] = {"is_approved": True}
            await query.edit_message_text(
                "Отлично! Когда начинается отпуск? (в формате ГГГГ-ММ-ДД)"
            )
            context.user_data["step"] = "start_date"
        else:
            await query.edit_message_text("Сначала согласуй даты с руководством.")
            return
    elif context.user_data.get("step") == "tickets_booked":
        context.user_data["vacation"]["tickets_booked"] = data == "yes"
        save_vacation(chat_id, context.user_data["vacation"])
        keyboard = [
            [InlineKeyboardButton("Начать планирование", callback_data="plan")],
            [InlineKeyboardButton("Показать планы", callback_data="show")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Отлично! Я сохранил твои планы. Чтобы посмотреть их, выбери действие:",
            reply_markup=reply_markup,
        )
        context.user_data.clear()


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if context.user_data.get("step") == "start_date":
        try:
            start_date = datetime.strptime(text, "%Y-%m-%d")
            if start_date < datetime.today():
                await update.message.reply_text(
                    "Дата начала отпуска не может быть раньше сегодняшнего дня."
                )
                return
            context.user_data["vacation"]["start_date"] = text
            await update.message.reply_text(
                "Когда заканчивается отпуск? (в формате ГГГГ-ММ-ДД)"
            )
            context.user_data["step"] = "end_date"
        except ValueError:
            await update.message.reply_text(
                "Неверный формат даты. Используйте формат ГГГГ-ММ-ДД."
            )
    elif context.user_data.get("step") == "end_date":
        try:
            end_date = datetime.strptime(text, "%Y-%m-%d")
            start_date = datetime.strptime(
                context.user_data["vacation"]["start_date"], "%Y-%m-%d"
            )
            if end_date <= start_date:
                await update.message.reply_text(
                    "Дата окончания отпуска не может быть раньше или равна дате начала."
                )
                return
            context.user_data["vacation"]["end_date"] = text
            await update.message.reply_text("Куда планируешь поехать?")
            context.user_data["step"] = "places_to_visit"
        except ValueError:
            await update.message.reply_text(
                "Неверный формат даты. Используйте формат ГГГГ-ММ-ДД."
            )
    elif context.user_data.get("step") == "places_to_visit":
        context.user_data["vacation"]["places_to_visit"] = text
        await update.message.reply_text("Что ты хочешь сделать во время отпуска?")
        context.user_data["step"] = "tasks"
    elif context.user_data.get("step") == "tasks":
        context.user_data["vacation"]["tasks"] = text
        keyboard = [
            [
                InlineKeyboardButton("Да", callback_data="yes"),
                InlineKeyboardButton("Нет", callback_data="no"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Забронированы ли билеты?", reply_markup=reply_markup
        )
        context.user_data["step"] = "tickets_booked"


async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    vacation = get_vacations(chat_id)
    if vacation:
        end_date = datetime.strptime(vacation[3], "%Y-%m-%d")
        days_left = (end_date - datetime.today()).days
        await query.edit_message_text(
            f"Даты отпуска: {vacation[2]} - {vacation[3]} (осталось {days_left} дней)\n"
            f"Места для посещения: {vacation[5]}\n"
            f"Задачи: {vacation[6]}\n"
            f"Билеты забронированы: {'Да' if vacation[7] else 'Нет'}"
        )
    else:
        await query.edit_message_text(
            "У тебя пока нет планов отпуска. Введи /start, чтобы начать."
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import logging

    logging.error(f"Exception while handling an update: {context.error}")
    await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте еще раз.")
