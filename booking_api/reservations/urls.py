from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (AnalysisByDateView, AnalysisView, GetAvailableHours,
                    ReservationViewSet, GetWeeklyDaysGraphView, GetGraphView)

router = DefaultRouter()
router.register("", ReservationViewSet)

urlpatterns = [
    path(
        "get_available_hours/", GetAvailableHours.as_view(), name="get_available_hours"
    ),
    path("analysis/", AnalysisView.as_view(), name="analysis"),
    path("analysis_by_date/", AnalysisByDateView.as_view(), name="analysis_by_date"),
    path("get_weekly_days_graph/", GetWeeklyDaysGraphView.as_view(), name="get_weekly_days_graph"),
    path('get_graph/', GetGraphView.as_view(), name='get_graph')
] + router.urls
