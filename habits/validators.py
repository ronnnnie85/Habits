from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class MaxDurationValueValidator:
    """
    Проверяет одно числовое значение (секунды).
    Используем для time_to_complete.
    """

    def __init__(self, max_seconds=120):
        self.max_seconds = max_seconds

    def __call__(self, value):
        if value is not None and value > self.max_seconds:
            raise ValidationError(
                f"Время выполнения не может быть больше {self.max_seconds} секунд."
            )


class PeriodValueValidator:
    """
    Проверяет одно числовое значение period.
    Используем для period.
    """

    def __init__(self, min_days=1, max_days=7):
        self.min_days = min_days
        self.max_days = max_days

    def __call__(self, value):
        if value < self.min_days or value > self.max_days:
            raise ValidationError(
                f"Периодичность должна быть от {self.min_days} до {self.max_days} дней."
            )


class RewardOrLinkedValidator:
    """
    Нельзя одновременно указывать вознаграждение и связанную привычку.
    Работает с dict данных (attrs).
    """

    def __call__(self, data: dict):
        reward = data.get("reward")
        related_habit = data.get("related_habit")
        if reward and related_habit:
            raise ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку."
            )


class RelatedHabitValidator:
    """
    В связанные привычки могут попадать только приятные привычки.
    data['related_habit'] — это объект Habit или None.
    """

    def __call__(self, data: dict):
        related_habit = data.get("related_habit")
        if related_habit and not getattr(related_habit, "is_pleasant", False):
            raise ValidationError(
                "Связанной привычкой может быть только приятная привычка."
            )


class PleasantHabitValidator:
    """
    У приятной привычки не может быть вознаграждения или связанной привычки.
    """

    def __call__(self, data: dict):
        is_pleasant = data.get("is_pleasant")
        reward = data.get("reward")
        related_habit = data.get("related_habit")
        if is_pleasant and (reward or related_habit):
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )


class HabitBusinessValidator:
    """
    Принимает dict (attrs + данные instance) и прогоняет через все объектные валидаторы.
    """

    def __init__(self):
        self.validators = [
            RewardOrLinkedValidator(),
            RelatedHabitValidator(),
            PleasantHabitValidator(),
        ]

    def __call__(self, data: dict):
        for validator in self.validators:
            validator(data)
