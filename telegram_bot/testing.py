import datetime as dt
import os
from datetime import datetime
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import requests
import threading
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler, CallbackQueryHandler
from constants import MONTHS, SCHEDULE, START_HOURS, WEEK_DAYS


def create_weekday_graph():
    """Создает график количества броней по дням недели."""
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path)
    # Получаем список бронирований через API
    response = requests.get(f"{os.getenv('API_URL')}/reservations/")
    reservations = response.json()
    # Группируем брони по дням недели
    weekday_counts = {}
    for reservation in reservations:
        date_str = reservation.get("date")  # Получаем строку с датой из API
        if date_str:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()  
            weekday = date_obj.weekday()
            weekday_name = date_obj.strftime("%A")[:3] #  Получаем сокращенное название дня недели
            if weekday_name in weekday_counts:
                weekday_counts[weekday_name] += 1
            else:
                weekday_counts[weekday_name] = 1

    # Переставляем дни недели в нужном порядке
    ordered_weekday_counts = {
        'Mon': weekday_counts.get('Mon', 0), 
        'Tue': weekday_counts.get('Tue', 0), 
        'Wed': weekday_counts.get('Wed', 0), 
        'Thu': weekday_counts.get('Thu', 0), 
        'Fri': weekday_counts.get('Fri', 0), 
        'Sat': weekday_counts.get('Sat', 0), 
        'Sun': weekday_counts.get('Sun', 0)
    }

    # Создаем график
    plt.bar(ordered_weekday_counts.keys(), ordered_weekday_counts.values())

    # Настройка графика
    plt.xlabel("День недели")
    plt.ylabel("Количество броней")
    plt.title("Количество броней по дням недели")

    # Запускаем график в отдельном потоке
    threading.Thread(target=plt.show).start()
    plt.show()

create_weekday_graph()
