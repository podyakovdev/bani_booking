import datetime as dt
import logging
import os

import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from constants import MONTHS, SCHEDULE, WEEK_DAYS
from utils import get_cost


(MAIN, RESERVATION, DASHBOARD, BOT_DISPELL,
 CHOOSING_DATE, CHOOSING_END_DATE) = range(6)

DAYS_POSSIBLE_TO_RESERVE = 10

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Переделать в кортежи если будет есть много памяти
reservations = {
    # 'user_id': {
    #     'gender': None,
    #     'date': None,
    #     'floor': None,
    #     'count': None,
    #     'start_hour': None,
    #     'finish_hour': None,
    #     'cost': None,
    # }
}


def get_gender(update, _):
    """Узнаем пол клиента."""
    query = update.callback_query
    query.answer()
    # user = update.callback_query.message.chat

    keyboard = [
        [InlineKeyboardButton("Женский", callback_data="GENDER:женский")],
        [InlineKeyboardButton("Мужской", callback_data="GENDER:мужской")],
        [InlineKeyboardButton("Главное меню", callback_data="START_OVER")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Выберите разряд", reply_markup=reply_markup)

    return RESERVATION


def get_date(update, _):
    """Предлагаем день."""
    query = update.callback_query
    query.answer()
    user = update.callback_query.message.chat

    # Сохраняем разряд
    reservations[user.id] = {
        "gender": query.data.split(":")[-1],
    }

    keyboard = []

    for i in range(DAYS_POSSIBLE_TO_RESERVE):
        day = dt.date.today() + dt.timedelta(days=i)

        # Если в этот день нет нужного разряда, то пропускаем
        if reservations[user.id]["gender"] not in SCHEDULE[day.isoweekday()].values():
            continue

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"{WEEK_DAYS[day.isoweekday()]}, " f"{day.day} {MONTHS[day.month]}",
                    callback_data=f"DATE:{day}",
                )
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton("Главное меню", callback_data="START_OVER"),
        ]
    )

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        "Выбран "
        f"{reservations[user.id]['gender']} разряд.\n"
        "Бронь доступна на ближайшие 10 дней.\n"
        # f'График разрядов:\n{SCHEDULE}'
        "Выберите день:",
        reply_markup=reply_markup,
    )

    return RESERVATION


def get_clients_count(update, _):
    """Сохраняем дату, этаж и узнаем количество гостей."""
    query = update.callback_query
    query.answer()
    user = query.message.chat

    reservations[user.id]["date"] = query.data.split(":")[-1]
    day = dt.datetime.strptime(reservations[user.id]["date"], "%Y-%m-%d")

    floor = next(
        (
            k
            for k, v in SCHEDULE[day.isoweekday()].items()
            if v == reservations[user.id]["gender"]
        ),
        None,
    )
    reservations[user.id]["floor"] = floor

    keyboard = [
        [InlineKeyboardButton("1", callback_data="COUNT:1")],
        [InlineKeyboardButton("2", callback_data="COUNT:2")],
        [InlineKeyboardButton("3", callback_data="COUNT:3")],
        [InlineKeyboardButton("4", callback_data="COUNT:4")],
        [InlineKeyboardButton("5", callback_data="COUNT:5")],
        [
            InlineKeyboardButton(
                "Нас больше 5, написать менеджеру", url="https://t.me/trtobeha/"
            )
        ],  # noqa
        [InlineKeyboardButton("Главное меню", callback_data="START_OVER")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        "Сколько нужно билетов?",
        reply_markup=reply_markup,
    )

    return RESERVATION


def get_start_hour(update, _):
    """Сохраняем день, предлагаем сеанс."""
    query = update.callback_query
    query.answer()
    user = update.callback_query.message.chat
    reservations[user.id]["count"] = query.data.split(":")[-1]

    keyboard = []

    day = dt.datetime.strptime(reservations[user.id]["date"], "%Y-%m-%d")

    for key, value in SCHEDULE[day.isoweekday()].items():
        if value == reservations[user.id]["gender"]:
            floor = key

    params = {
        "date": reservations[user.id]["date"],
        "floor": str(floor),
        "count": reservations[user.id]["count"],
    }

    available_hours = eval(
        requests.get(
            f"{os.getenv('API_URL')}/reservations/get-available-hours/", params=params
        ).text
    )
    # available_hours = {
    #     14: [16, 17, 18, 19, 20, 21, 22],
    #     15: [17, 18, 19, 20, 21, 22],
    #     16: [18, 19, 20, 21, 22]
    # }
    reservations[user.id]["reservations"] = available_hours
    for hour in available_hours.keys():
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"{str(hour)}:00", callback_data=f"START_HOUR:{hour}"
                )
            ]
        )
    keyboard.append([InlineKeyboardButton("Главное меню", callback_data="START_OVER")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Если мест вообще нет:
    if len(keyboard) == 1:
        query.edit_message_text(
            "В выбранный вами день " "недостаточно свободных мест.",
            reply_markup=reply_markup,
        )
        return RESERVATION

    day = dt.datetime.strptime(reservations[user.id]["date"], "%Y-%m-%d")
    query.edit_message_text(
        "Количество билетов: "
        f"{reservations[user.id]['count']}.\n"
        f"Дата: {WEEK_DAYS[day.isoweekday()]}, "
        f"{day.day} {MONTHS[day.month]}\n\n"
        "Выберите начало сеанса:",
        reply_markup=reply_markup,
    )

    return RESERVATION


def get_finish_hour(update, _):
    """Сохраняем начало сеанса, предлагаем время окончания."""
    query = update.callback_query
    query.answer()
    user = update.callback_query.message.chat

    start_hour = query.data.split(":")[1]
    reservations[user.id]["start_hour"] = start_hour

    keyboard = []
    finish_hours = reservations[user.id]["reservations"][f"{start_hour}"]
    for h in finish_hours:
        keyboard.append(
            [InlineKeyboardButton(f"{h}:00", callback_data=f"FINISH_HOUR:{h}")]
        )

    keyboard.append(
        [
            InlineKeyboardButton("Главное меню", callback_data="START_OVER"),
        ]
    )
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        "Выберите конец сеанса: \n",
        reply_markup=reply_markup,
    )

    return RESERVATION


def get_payment(update, _):
    """Сохраняем кол-во часов, предлагаем оплату."""
    query = update.callback_query
    query.answer()
    user = update.callback_query.message.chat

    reservations[user.id]["finish_hour"] = query.data.split(":")[-1]
    keyboard = [
        [
            InlineKeyboardButton("Оплатить онлайн", callback_data="PAYMENT:True"),
            InlineKeyboardButton("В главное меню", callback_data="START_OVER"),
        ]
    ]

    if user.id in eval(os.getenv("ADMIN_IDs")):
        keyboard.insert(
            0, [InlineKeyboardButton("Оплата наличными", callback_data="PAYMENT:True")]
        )

    day = dt.datetime.strptime(reservations[user.id]["date"], "%Y-%m-%d")

    start_hour = reservations[user.id]["start_hour"]
    finish_hour = reservations[user.id]["finish_hour"]
    count = reservations[user.id]["count"]
    gender = reservations[user.id]["gender"]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        "Вы собираетесь оплатить:\n\n"
        f"{WEEK_DAYS[day.isoweekday()]}, "
        f"{day.day} {MONTHS[day.month]}\n"
        f"{gender.capitalize()} разряд.\n"
        f"Этаж {reservations[user.id]['floor']}.\n"
        f"Количество человек: {count}\n"
        f"Сеанс с {start_hour}:00"
        f" до {finish_hour}:00\n\n"
        f"Общая стоимость {get_cost(reservations[user.id])} руб.",  # noqa
        reply_markup=reply_markup,
    )
    return RESERVATION


def save_payment(update, _):
    query = update.callback_query
    query.answer()
    user = update.callback_query.message.chat

    data = {
        "date": reservations[user.id]["date"],
        "user": user.id,
        "gender": reservations[user.id]["gender"],
        "floor": reservations[user.id]["floor"],
        "start_hour": reservations[user.id]["start_hour"],
        "finish_hour": reservations[user.id]["finish_hour"],
        "cost": get_cost(reservations[user.id]),
        "confirmed": True,
    }

    # Создать запись в БД сразу, до оплаты, чтобы за время оплаты
    # место не стало занято другим пользователем.
    try:
        requests.post(f"{os.getenv('API_URL')}/reservations/", data=data)
    except Exception as e:
        logger.critical(e)

    keyboard = [
        [
            InlineKeyboardButton("Главное меню", callback_data="START_OVER"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        "Запись оплачена, будем вас ждать!\n"
        "Активные записи вы можете отслеживать "
        "в личном кабинете",
        reply_markup=reply_markup,
    )
    return RESERVATION
