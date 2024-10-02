# import re
import copy
import logging
import os
import sys
import time

import requests
from dotenv import load_dotenv
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      InputMediaDocument, InputMediaPhoto, ParseMode, File)
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Updater, MessageHandler,
                          Filters)

from constants import ABOUT_TEXT, CONTACTS_TEXT
from dashboard import dashboard, handle_start_date, get_analisys_by_date, show_analisys_by_date
from reservations import (get_clients_count, get_date, get_finish_hour,
                          get_gender, get_payment, get_start_hour,
                          save_payment)
from utils import (check_tokens, get_profile_data, get_reservations_history,
                   registration)

(MAIN, RESERVATION, DASHBOARD, BOT_DISPELL,
 CHOOSING_DATE, CHOOSING_END_DATE) = range(6)

RANKS = {
    0: "Новичок",
    6: "Рядовой",
    20: "Опытный",
    50: "Гвардеец",
    75: "Сталевар",
    100: "Генсек",
}


BASE_KEYBOARD = [
    [
        InlineKeyboardButton("Забронировать", callback_data="GET_GENDER"),
        InlineKeyboardButton("Мой профиль", callback_data="MY_PROFILE"),
    ],
    [InlineKeyboardButton("Кабинетная планировка, 2 этаж", callback_data="2_FLOOR")],
    [
        InlineKeyboardButton("Русский стиль, 3 этаж", callback_data="3_FLOOR"),
    ],
    [
        InlineKeyboardButton("Важное о нас", callback_data="ABOUT"),
        InlineKeyboardButton("Контакты", callback_data="CONTACTS"),
    ],
]


def start(update, _):
    """Команда `/start`."""
    user = update.message.from_user
    logger.info(f"Пользователь {user.first_name}-id{user.id} начал разговор")

    if user["is_bot"]:
        return BOT_DISPELL

    registration(user)

    keyboard = copy.deepcopy(BASE_KEYBOARD)

    if user.id in eval(os.getenv("ADMIN_IDs")):
        keyboard.append(
            [InlineKeyboardButton("Админ-панель", callback_data="DASHBOARD")]
        )

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        text=f"{user.first_name}, приветствую тебя в Измайловских банях!\n"
        "Здесь можно забронировать место на желаемый сеанс.\n",
        reply_markup=reply_markup,
    )

    return MAIN


def start_over(update, _):
    """Начальное состояние меню для возвратов."""
    query = update.callback_query
    query.answer()
    user = update.callback_query.message.chat

    keyboard = copy.deepcopy(BASE_KEYBOARD)

    if user.id in eval(os.getenv("ADMIN_IDs")):
        keyboard.append(
            [InlineKeyboardButton("Админ-панель", callback_data="DASHBOARD")]
        )

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"{user.first_name}, "
        "приветствуем в Измайловских банях!\n"
        "Здесь можно забронировать место"
        " на желаемый сеанс.\n",
        reply_markup=reply_markup,
    )

    return MAIN


def my_profile(update, _):
    """Показ нового выбора кнопок."""
    query = update.callback_query
    query.answer()
    user = update.callback_query.message.chat
    keyboard = [
        [
            InlineKeyboardButton(
                "История посещений", callback_data="RESERVATIONS_HISTORY"
            )
        ],
        [InlineKeyboardButton("Назад", callback_data="START_OVER")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    profile_data, count = get_profile_data(user)
    rank = ""

    for hour_value in sorted(RANKS.keys()):
        if hour_value < count:
            rank = RANKS[hour_value]
        continue

    next_rank = ""
    hours_to_next_rank = 0

    for hour_value in sorted(RANKS.keys()):
        if hour_value > count:
            next_rank = RANKS[hour_value]
            hours_to_next_rank = hour_value - count
            break
    query.edit_message_text(
        text=f"Номер пользователя {user.id}\n\n"
        f"Всего часов напарено: {count}\n"
        f"Звание: {rank}\n"
        f"Часов до звания <b>{next_rank}</b>: "
        f"{hours_to_next_rank}\n"
        f"{profile_data}",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML,
    )
    return MAIN


def reservations_history(update, _):
    query = update.callback_query
    query.answer()
    user = update.callback_query.message.chat

    keyboard = [
        [InlineKeyboardButton("Назад", callback_data="MY_PROFILE")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = get_reservations_history(user)

    if text is None:
        text = "😔 К сожалению, вы пока у нас не были 😔"
    query.edit_message_text(
        text="Последние 10 посещений:\n\n" + text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )

    return MAIN


def about(update, _):
    query = update.callback_query
    query.answer()

    keyboard = [
        [InlineKeyboardButton("Назад", callback_data="START_OVER")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=ABOUT_TEXT,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )

    return MAIN


def contacts(update, _):
    """Контакты."""
    query = update.callback_query
    query.answer()

    keyboard = [
        [InlineKeyboardButton("Назад", callback_data="START_OVER")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=CONTACTS_TEXT,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )

    return MAIN


def bot_dispell(update, _):
    pass


def second_floor(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id

    file_path1 = "images/2/26.jpg"
    file_path2 = "images/2/28.jpg"
    file_path3 = "images/2/31.jpg"
    file_path4 = "images/2/36.jpg"

    media_group = [
        InputMediaPhoto(media=open(file_path1, "rb"),
                        caption="Это описание фото?"),
        InputMediaPhoto(media=open(file_path2, "rb"),
                        caption="Это описание фото?"),
        InputMediaPhoto(media=open(file_path3, "rb"),
                        caption="Это описание фото?"),
        InputMediaPhoto(media=open(file_path4, "rb"),
                        caption="Это описание фото?"),
    ]

    keyboard = [
        [InlineKeyboardButton("Назад", callback_data="START_OVER")],
    ]

    text = (
        "Более вместительный зал из двух, которыми располагают"
        "Измайловские бани, рассчитан на 36 мест, расположен "
        "на 2 этаже, в правом крыле здания.\n\n"
        "Перед входом в разряд имеется бар-буфет и просторный"
        " зал с несколькими столами. Раздевалка состоит из "
        "больших кабинок с бревенчатыми перегородками, "
        "каждая на 6 человек. Все отделано деревом и производит "
        "приятное впечатление все той же добротности. За комнатой"
        " отдыха следует помывочный зал, с теплыми скамейками из мрамора, "
        "душевыми кабинами и купелью с ледяной водой.\n\n"
        "За моечным помещением находится сердце бани - парилка, в которой "
        "построена прекрасная каменная печь, размером от пола до "
        "потолка. В парной царят ароматы австралийского эвкалипта, "
        "и русской пихты, которые подарят Вам самые положительные эмоции!"
        "Приглашаем Вас лично посетить нашу баню, стилизованную "
        "под русскую избу, и украшенную хохломской росписью.\n\n"
        "Стоимость посещения 600 рублей за час."
    )
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_media_group(chat_id=chat_id, media=media_group)
    context.bot.send_message(
        chat_id=chat_id, text=text, reply_markup=reply_markup,
        parse_mode="Markdown"
    )

    return MAIN


def third_floor(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id

    file_path1 = "images/3/10.jpg"
    file_path2 = "images/3/22.jpg"

    media_group = [
        InputMediaPhoto(media=open(file_path1, "rb"),
                        caption="Это описание фото?"),
        InputMediaPhoto(media=open(file_path2, "rb"),
                        caption="Это описание фото?"),
    ]

    keyboard = [
        [InlineKeyboardButton("Назад", callback_data="START_OVER")],
    ]

    text = (
        "Это престижный небольшой разряд, где комфортно"
        " размещается до 23 человек. Зал расположен на 3-м "
        "этаже, в левом крыле здания.\n\n"
        "Помещение состоит из трех уютных отдельных кабинетов "
        "на 10, 6, и 5 человек.\n\n"
        "В данном разряде небольшая парная с отличным паром, "
        "всегда наполненная ароматами полыни, мяты и донника, мыльня "
        "с теплыми скамейками из мрамора и душевыми кабинами; купель с "
        "ледяной водой.\n\nТак же для Вас работает бар, где всегда имеется"
        " большой выбор различных закусок, прохладительных напитков, "
        "горячий чай. Здесь всегда царят комфорт и "
        "душевная обстановка.\n\n"
        "Стоимость посещения 750 рублей за час."
    )
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_media_group(chat_id=chat_id, media=media_group)
    context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )

    return MAIN


if __name__ == "__main__":

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    logger = logging.getLogger(__name__)

    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(dotenv_path):
        logger.critical("Не найден файл .env")
    load_dotenv(dotenv_path)

    if not check_tokens(os.getenv("TELEGRAM_TOKEN")):
        logger.critical("Проблема с переменными в .env")
        sys.exit()

    API_URL = os.getenv('API_URL')
    updater = Updater(os.getenv("TELEGRAM_TOKEN"))
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN: [
                CallbackQueryHandler(my_profile, pattern="MY_PROFILE"),
                CallbackQueryHandler(about, pattern="ABOUT"),
                CallbackQueryHandler(start_over, pattern="START_OVER"),
                CallbackQueryHandler(contacts, pattern="CONTACTS"),
                CallbackQueryHandler(get_gender, pattern="GET_GENDER"),
                CallbackQueryHandler(dashboard, pattern="DASHBOARD"),
                CallbackQueryHandler(second_floor, pattern="2_FLOOR"),
                CallbackQueryHandler(third_floor, pattern="3_FLOOR"),
                CallbackQueryHandler(
                    reservations_history, pattern="RESERVATIONS_HISTORY"
                ),
            ],
            RESERVATION: [
                CallbackQueryHandler(get_date, pattern=r"^GENDER:"),
                CallbackQueryHandler(get_clients_count, pattern=r"^DATE:"),
                CallbackQueryHandler(get_start_hour, pattern=r"^COUNT:"),
                CallbackQueryHandler(get_finish_hour, pattern=r"^START_HOUR:"),
                CallbackQueryHandler(get_payment, pattern=r"^FINISH_HOUR:"),
                CallbackQueryHandler(save_payment, pattern=r"PAYMENT:"),
                CallbackQueryHandler(start_over, pattern="START_OVER"),
            ],
            BOT_DISPELL: [
                CallbackQueryHandler(bot_dispell, pattern="BOT_DISPELL"),
            ],
            DASHBOARD: [
                CallbackQueryHandler(start_over, pattern="START_OVER"),
                CallbackQueryHandler(get_analisys_by_date,
                                     pattern="ANALISYS_BY_DATE"),
            ],
            CHOOSING_DATE: [
                MessageHandler(Filters.text & ~Filters.command,
                               handle_start_date),
                CallbackQueryHandler(dashboard, pattern="DASHBOARD")],
            CHOOSING_END_DATE: [
                MessageHandler(Filters.text & ~Filters.command,
                               show_analisys_by_date),
                CallbackQueryHandler(dashboard, pattern="DASHBOARD"),]
        },
        fallbacks=[CommandHandler("start", start)],
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
