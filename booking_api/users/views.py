from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from reservations.models import Reservation

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserReservationCountView(APIView):
    """
    Возвращает количество подтвержденных броней для пользователя.
    """

    def get(self, request, user_id):
        try:
            now = timezone.now()
            # Получаем все подтвержденные брони для пользователя
            confirmed_reservations = Reservation.objects.filter(
                user__telegram_id=user_id, confirmed=True
            )

            future_reservations = Reservation.objects.filter(
                user__telegram_id=user_id, date__gt=now, confirmed=True
            )
            hour_count = 0
            for r in confirmed_reservations:
                hours = int(r.finish_hour) - int(r.start_hour)
                hour_count += hours
            serialized_reservations = [
                {
                    "date": reservation.date,
                    "floor": reservation.floor,
                    "start_hour": reservation.start_hour,
                    "finish_hour": reservation.finish_hour,
                    "cost": reservation.cost,
                    "confirmed": reservation.confirmed,
                }
                for reservation in future_reservations
            ]
            return Response(
                {
                    "hour_count": hour_count,
                    "future_bookings": serialized_reservations,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserReservationHistoryView(APIView):
    """
    Возвращает историю бронирований пользователя.
    """

    def get(self, request, user_id):
        """
        Обрабатывает GET-запрос.
        """
        try:
            now = timezone.now()
            reservations = Reservation.objects.filter(
                user__telegram_id=user_id, confirmed=True, date__lt=now
            )[:10]
            serialized_reservations = [
                {
                    "date": reservation.date,
                    "floor": reservation.floor,
                    "start_hour": reservation.start_hour,
                    "finish_hour": reservation.finish_hour,
                    "cost": reservation.cost,
                    "confirmed": reservation.confirmed,
                }
                for reservation in reservations
            ]
            return Response(
                {"user_history": serialized_reservations}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
