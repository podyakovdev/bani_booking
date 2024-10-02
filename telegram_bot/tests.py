import json
import os
import random

import requests
from dotenv import load_dotenv

from utils import registration

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if not os.path.exists(dotenv_path):
    print("Не найден файл .env")
load_dotenv(dotenv_path)


url = os.getenv("API_URL")


# {
#     'username': 'trtobeha',
#     'id': 286984778,
# }


# mock_user = {
#     'username': 'trtobeha123',
#     'id': 286984722,
# }
# # registration(mock_user)

# # Создание моковых записей
# mock_reservations = []


# data = {
#         "user": "286984778",
#         "date": "2024-08-07",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(20):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)

# data = {
#         "user": "286984778",
#         "date": "2024-08-08",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(20):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)

# data = {
#         "user": "286984778",
#         "date": "2024-08-09",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(30):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)

# data = {
#         "user": "286984778",
#         "date": "2024-08-10",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(30):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)

# data = {
#         "user": "286984778",
#         "date": "2024-08-11",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(20):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)

# data = {
#         "user": "286984778",
#         "date": "2024-08-12",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(20):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)

# data = {
#         "user": "286984778",
#         "date": "2024-08-13",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(20):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)

# data = {
#         "user": "286984778",
#         "date": "2024-08-14",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(20):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)

# data = {
#         "user": "286984778",
#         "date": "2024-08-15",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(25):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)

# data = {
#         "user": "286984778",
#         "date": "2024-08-16",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(30):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)

# data = {
#         "user": "286984778",
#         "date": "2024-08-17",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(30):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)

# data = {
#         "user": "286984778",
#         "date": "2024-08-18",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(20):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)

# data = {
#         "user": "286984778",
#         "date": "2024-08-19",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(10):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)

# data = {
#         "user": "286984778",
#         "date": "2024-08-20",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(15):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)

# data = {
#         "user": "286984778",
#         "date": "2024-08-21",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(20):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)

# data = {
#         "user": "286984778",
#         "date": "2024-08-22",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(20):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)

# data = {
#         "user": "286984778",
#         "date": "2024-08-23",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(31):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)

# data = {
#         "user": "286984778",
#         "date": "2024-08-24",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(19):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)

# data = {
#         "user": "286984778",
#         "date": "2024-08-25",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(18):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)

# data = {
#         "user": "286984778",
#         "date": "2024-08-26",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(15):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)

# data = {
#         "user": "286984778",
#         "date": "2024-08-27",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(16):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)
# data = {
#         "user": "286984778",
#         "date": "2024-08-28",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(14):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)
# data = {
#         "user": "286984778",
#         "date": "2024-08-29",
#         "floor": 3,
#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(22):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)
# data = {
#         "user": "286984778",
#         "date": "2024-08-30",
#         "floor": 3,

#         "start_hour": 18,
#         "finish_hour": 22,
#         "cost": 2200,
#         "confirmed": "True"
# }
# for i in range(29):
#     requests.post(f'{os.getenv('API_URL')}/reservations/',
#                   data=data)


data = {
    "user": "286984778",
    "date": "2024-08-31",
    "floor": 3,
    "gender": "мужской",
    "start_hour": 18,
    "finish_hour": 22,
    "cost": 2200,
    "confirmed": "True",
}
for i in range(28):
    res = requests.post(f"{os.getenv('API_URL')}/reservations/", data=data)
    print(res.text)
