import datetime as dt
import os
from datetime import datetime
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler, CallbackQueryHandler
from constants import MONTHS, SCHEDULE, START_HOURS, WEEK_DAYS


(MAIN, RESERVATION, DASHBOARD, BOT_DISPELL,
 CHOOSING_DATE, CHOOSING_END_DATE) = range(6)

choose_date = {}
# choose_date = {
#     "start_date": "2024.31.08",
#     "fininsh_date": "2024.31.08"
#


def dashboard(update, _):
    """Админ-панель."""
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path)

    query = update.callback_query
    query.answer()

    keyboard = [
        # [InlineKeyboardButton("Отчет по выручке",
        #                       callback_data='START_OVER')],
        # [InlineKeyboardButton("Аналитика посещений",
        #                       allback_data='START_OVER')],
        [InlineKeyboardButton("Аналитика в выбранный период",
                              callback_data='ANALISYS_BY_DATE')],
        [InlineKeyboardButton("Назад", callback_data="START_OVER")],
    ]
    text = ''
    res = requests.get(
        f'{os.getenv('API_URL')}/reservations/analysis/'
    ).json()
    create_weekday_graph()
    text = ('АДМИНИСТРАТИВНАЯ ПАНЕЛЬ.\n\n'
            f'Уникальных клиентов: {res['users_count']}\n'
            f'Всего бронирований: {res['total_reservations']}\n'
            f''
            f'\nАналитика за этот месяц:\n'
            f'Бронирований: {res['reservations_this_month']}\n'
            f'Выручка с билетов: <b>'
            f'{'{:,}'.format(res['earned_this_month']).replace(',', ' ')}</b> руб.'
            f''
            )

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML,
        # disable_web_page_preview=True,
    )

    return DASHBOARD


def get_analisys_by_date(update, _):
    """Получаем аналитику в выбранный период. Спрашиваем дату ОТ. """
    query = update.callback_query
    query.answer()
    # user = update.callback_query.message.chat

    keyboard = [
        [InlineKeyboardButton("Назад", callback_data="DASHBOARD")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Введите дату начала в формате 2023-12-31",
                            reply_markup=reply_markup)

    return CHOOSING_DATE


def handle_start_date(update, context):

    keyboard = [
        [InlineKeyboardButton("Назад", callback_data="DASHBOARD")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    user_input = update.message.text
    try:
        choose_date['start_date'] = datetime.datetime.strptime(
            user_input, '%Y-%m-%d'
        ).date()
        update.message.reply_text(
            f'Дата начала: {choose_date['start_date']}. '
            'Введите дату окончания в том же формате.',
            reply_markup=reply_markup)
        return CHOOSING_END_DATE

    except ValueError:
        update.message.reply_text(
            "Неверный формат даты. "
            "Пожалуйста, введите дату в формате 2023-12-31"
        )
        return CHOOSING_DATE


def show_analisys_by_date(update, _):
    """ Сохраняем дату окончания и выводим аналитику. """

    keyboard = [
        [InlineKeyboardButton("Назад", callback_data="DASHBOARD")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    user_input = update.message.text
    try:
        choose_date['finish_date'] = datetime.datetime.strptime(
            user_input, '%Y-%m-%d').date()

        # Тут получаем аналитику с бэкенда.

        # Тут выводим аналитику с бэкенда.

        update.message.reply_text(
            f'Выбран период с {choose_date['start_date']} до'
            f'{choose_date['finish_date']}.\n\nВаша аналитика: ƒ',
            reply_markup=reply_markup)
        return MAIN
    except ValueError:
        update.message.reply_text("Неверный формат даты. Пожалуйста, "
                                  "введите дату в формате 2023-12-31")
        return CHOOSING_END_DATE
