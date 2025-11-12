from rest_framework import generics, permissions, viewsets

from .models import Habit
from .pagination import MyPagination
from .permissions import IsOwner
from .serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """CRUD привычек текущего пользователя."""

    serializer_class = HabitSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    pagination_class = MyPagination

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)


class PublicHabitListView(generics.ListAPIView):
    """Список публичных привычек."""

    serializer_class = HabitSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
