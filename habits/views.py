from rest_framework import viewsets, generics, permissions
from .serializers import HabitSerializer
from .permissions import IsOwner
from .models import Habit


class HabitViewSet(viewsets.ModelViewSet):
    """CRUD привычек текущего пользователя."""

    serializer_class = HabitSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)


class PublicHabitListView(generics.ListAPIView):
    """Список публичных привычек."""

    serializer_class = HabitSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
