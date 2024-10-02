from rest_framework import viewsets, permissions
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.http import JsonResponse
from django.db.models import Sum
import os
import io
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from dotenv import load_dotenv
import pytz
from users.models import User
from django.utils import timezone
import json
import threading
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse


START_HOURS = [8, 10, 12, 14, 16, 18, 20, 22]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.AllowAny]


class GetAvailableHours(APIView):
    """ Получение доступных сеансов для записи. """

    def get(self, request):
        """ Не работает. Переделать полностью"""
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                   '.env')
        load_dotenv(dotenv_path)

        date = request.GET.get('date')
        floor = int(request.GET.get('floor'))
        count = int(request.GET.get('count'))
        # Проверка на максимальное количество человек
        if count > int(os.getenv(f'FLOOR_{floor}_LIMIT')):
            return JsonResponse({'error': f'Максимальное количество человек'
                                          ' - '
                                          f'{os.getenv(f'FLOOR_{floor}_LIMIT')}.'},
                                status=400)

        # Получение всех бронирований на заданную дату и этаж
        reservations = Reservation.objects.filter(date=date, floor=floor)

        # Если выбран понедельник, то доступны сеансы только с 14:00
        day = datetime.strptime(date, '%Y-%m-%d')
        start_hour = 8
        if day.isoweekday() == 1:
            start_hour = 14

        # Убираем сегодняшние сеансы, которые уже начались
        timezone = pytz.timezone('Europe/Moscow')
        if day.date() == datetime.today().date():
            start_hour = datetime.now(timezone).hour + 1

        # Создание списка всех часов в день (с 8 до 20)
        all_hours = list(range(start_hour, 21))

        # Узнаем, сколько человек уже записано на каждый часовой интервал.
        # создаем счетчик людей
        people_counter = {}
        for hour in all_hours:
            people_counter[hour] = 0

        for hour in all_hours:
            for reservation in reservations:
                if reservation.start_hour <= hour and reservation.finish_hour >= hour + 1:
                    people_counter[hour] += 1
        # people_counter = {
        #     8: 10,
        #     10: 5,
        #     12: 4,
        #     14: 14,
        #     16: 22,
        #     18: 27,
        #     20: 30
        # }

        # Проверим помещается ли необходимое количество человек в лимит
        available_start_hours = []
        for hour in people_counter.keys():
            if int(people_counter[hour]) + count <= int(os.getenv(f'FLOOR_{floor}_LIMIT')):
                available_start_hours.append(hour)
        print(available_start_hours)
        
        intervals = []
        start = available_start_hours[0]
        current_interval = [start]

        for i in range(1, len(available_start_hours)):
            if available_start_hours[i] == available_start_hours[i - 1] + 1:
                current_interval.append(available_start_hours[i])
        else:
            intervals.append((start, current_interval[-1]))
            start = available_start_hours[i]
            current_interval = [start]
        # intervals = [(8, 20)]

        for interval in intervals[:]:
            if interval[1] - interval[0] < 2:
                intervals.remove(interval)

        print(intervals)

        return Response(
                data=people_counter,
                status=status.HTTP_200_OK
            )
#
#
###
    # available_sessions = {
    #     14: [16, 17, 18, 19, 20, 21, 22],
    #     15: [17, 18, 19, 20, 21, 22],
    #     16: [18, 19, 20, 21, 22]
    # }


class AnalysisView(APIView):
    def get(self, request):
        now = timezone.now()

        try:
            # Общее число клиентов:
            users_count = User.objects.all().count()

            # Общее число сделанных броней
            total_reservations = Reservation.objects.all().count()

            # Броней за этот месяц
            reservations = Reservation.objects.filter(
                confirmed=True,
                date__month=now.month
                # date__lt=now
            )
            now = timezone.now()
            earned_this_month = Reservation.objects.filter(
                date__month=now.month,
                confirmed=True
            ).aggregate(Sum('cost'))['cost__sum']
            print(earned_this_month)

            data = {
                "users_count": users_count,
                "total_reservations": total_reservations,
                "reservations_this_month": reservations.count(),
                "earned_this_month": earned_this_month,
            }
            return Response(
                data=data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    # data = {
    #     "users_count": users_count,
    #     "total_reservations": total_reservations,
    #     "earned_this_month": earned_this_month,
    # }
    # return JsonResponse(data)


class AnalysisByDateView(APIView):
    """ Получение аналитики за временной промежуток. """

    def get(self, response):
        # now = timezone.now()

        start_date = response.data['start_date']
        finish_date = response.data['finish_date']

        try:
            # Получим оплаченные записи за выбранный период
            reservations = Reservation.objects.filter(
                confirmed=True,
                date__gt=start_date,
                date__lt=finish_date
            )

            data = {
                "reservations_count": reservations.count(),  # Количество броней # noqa
                "total_money": reservations.aggregate(  # Получено с них денег
                    Sum('cost'))['cost__sum']
            }

            return Response(
                data=data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class GetWeeklyDaysGraphView(APIView):
    def get(self, request):
        """
        Создает график количества броней по дням недели и возвращает его в виде изображения.
        """
        # Получаем список бронирований из модели
        reservations = Reservation.objects.all()

        # Группируем брони по дням недели
        weekday_counts = {}
        for reservation in reservations:
            weekday_name = reservation.date.strftime("%A")[:3]
            if weekday_name in weekday_counts:
                weekday_counts[weekday_name] += 1
            else:
                weekday_counts[weekday_name] = 1

        # Переставляем дни недели в нужном порядке
        ordered_weekday_counts = {
            'ПН': weekday_counts.get('Mon', 0),
            'ВТ': weekday_counts.get('Tue', 0),
            'СР': weekday_counts.get('Wed', 0),
            'ЧТ': weekday_counts.get('Thu', 0),
            'ПТ': weekday_counts.get('Fri', 0),
            'СБ': weekday_counts.get('Sat', 0),
            'ВС': weekday_counts.get('Sun', 0)
        }
        # Вычисляем среднее количество броней для каждого дня недели
        #
        # Как посчитать сколько понедельников в временном диапазоне?

        # Создаем график
        matplotlib.use('agg')
        plt.bar(average_weekday_counts.keys(), average_weekday_counts.values())

        # Настройка графика
        plt.xlabel("День недели")
        plt.ylabel("Среднее количество броней")
        plt.title("Среднее количество броней по дням недели")

        # Сохраняем график в буфер памяти
        # buf = io.BytesIO()
        # plt.savefig(buf, format='jpeg')
        plt.savefig('graphs/weekly_reservations.jpeg', format='jpeg')  # Сохранение в файл
        plt.close()

        image_url = reverse('get_graph') + '?image_name=weekly_reservations.jpeg'

        return redirect(image_url)


class GetGraphView(APIView):
    def get(self, request):
        image_name = request.GET.get('image_name')
        if image_name:
            try:
                with open(f'graphs/{image_name}', 'rb') as f:
                    image_data = f.read()
                return HttpResponse(image_data, content_type='image/jpeg')
            except FileNotFoundError:
                return HttpResponse('Изображение не найдено', status=404)
        else:
            return HttpResponse('Не указано имя изображения', status=400)
