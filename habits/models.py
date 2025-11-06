from django.conf import settings
from django.db import models


class Habit(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
    )
    place = models.CharField(max_length=255, verbose_name="Место выполнения")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=255, verbose_name="Действие")

    is_pleasant = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )
    related_habit = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="linked_to",
        verbose_name="Связанная привычка",
    )

    period = models.PositiveSmallIntegerField(default=1, verbose_name="Периодичность")
    reward = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Вознаграждение"
    )
    time_to_complete = models.PositiveSmallIntegerField(
        default=60, verbose_name="Время на выполнение"
    )
    is_public = models.BooleanField(default=False, verbose_name="Публичная")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

        ordering = ("-action",)

    def __str__(self):
        return f"я буду {self.action} в {self.time} в {self.place}"
