from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (UserReservationCountView, UserReservationHistoryView,
                    UserViewSet)

router = DefaultRouter()
router.register("", UserViewSet)


urlpatterns = [
    path("<int:user_id>/start_info/", UserReservationCountView.as_view()),
    path("<int:user_id>/get_user_history/", UserReservationHistoryView.as_view()),
] + router.urls
