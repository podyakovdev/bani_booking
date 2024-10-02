import json
import logging
import os
import time
from http import HTTPStatus

import requests

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def check_tokens(TELEGRAM_TOKEN):
    if TELEGRAM_TOKEN:
        return True


def registration(user):
    # готово
    data = {
        "telegram_id": user.id,
        "username": user["username"],
    }
    headers = {"Content-Type": "application/json"}
    json_data = json.dumps(data)

    try:
        r = requests.get(
            f"{os.getenv('API_URL')}/users/{user.id}/",
        )
        if r.status_code == HTTPStatus.OK:
            return True
    except Exception as e:
        logger.critical(e)

    i = 1
    while True:
        try:
            r = requests.post(
                f"{os.getenv('API_URL')}/users/",
                data=json_data,
                headers=headers,
            )
            print(r.text)
            if r.status_code == HTTPStatus.CREATED:
                logger.info(
                    "Зарегистрирован новый " f"пользователь {user['username']}!"
                )
                return True
        except Exception as e:
            logger.critical(
                f"ПОПЫТКА {i} - Ошибка во время запроса "
                f"на регистрацию в Django: {e}"
            )
        i += 1
        time.sleep(2)


def get_cost(data):
    start_hour = int(data["start_hour"])
    finish_hour = int(data["finish_hour"])
    count = int(data["count"])
    hour_cost = int(os.getenv("HOUR_COST"))

    return hour_cost * (finish_hour - start_hour) * count


def get_start_text(user) -> str:
    text = (
        f"{user.username}, добро пожаловать в Измайловские бани!"
        f"Женский день: среда"
        f"Все остальные мужские"
    )
    return text


def get_profile_data(user):
    try:
        res = requests.get(
            f"{os.getenv('API_URL')}/users/" f"{int(user.id)}/start_info/"
        ).json()
        future_reservations_text = ""
        if len(res["future_bookings"]) != 0:
            future_reservations_text += "\n\nПланируемые визиты:\n"

            for reservation in res["future_bookings"]:
                date = reservation["date"]
                floor = reservation["floor"]
                start_hour = reservation["start_hour"]
                finish_hour = reservation["finish_hour"]

                future_reservations_text += (
                    f"Этаж: {floor}\n"
                    f"📆 {date}\n"
                    f"⏰ с {start_hour}:00 до "
                    f"{finish_hour}:00\n\n"
                )

        return future_reservations_text, int(res["hour_count"])
    except Exception as e:
        logger.critical(f"{e}")


def get_reservations_history(user):
    try:
        res = requests.get(
            f"{os.getenv('API_URL')}/users/" f"{int(user.id)}/get_user_history/"
        ).json()
        history_text = ""
        if len(res["user_history"]) != 0:
            for r in res["user_history"]:
                date = r["date"]
                floor = r["floor"]
                start_hour = r["start_hour"]
                finish_hour = r["finish_hour"]

                history_text += (
                    f"Этаж: {floor}\n"
                    f"📆 {date}\n"
                    f"⏰ с {start_hour}:00 до "
                    f"{finish_hour}:00\n\n"
                )

            return history_text
    except Exception as e:
        logger.critical(f"{e}")
