from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HabitViewSet, PublicHabitListView

app_name = "habits"

router = DefaultRouter()
router.register("habits", HabitViewSet, basename="habit")

urlpatterns = [
    path("habits/public/", PublicHabitListView.as_view(), name="public-habits"),
]

urlpatterns += router.urls
