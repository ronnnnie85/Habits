from rest_framework import serializers

from .models import Habit
from .validators import (
    HabitBusinessValidator,
    MaxDurationValueValidator,
    PeriodValueValidator,
)


class HabitSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    time_to_complete = serializers.IntegerField(
        validators=[MaxDurationValueValidator(max_seconds=120)]
    )

    period = serializers.IntegerField(
        validators=[PeriodValueValidator(min_days=1, max_days=7)]
    )

    class Meta:
        model = Habit
        fields = (
            "id",
            "owner",
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "period",
            "reward",
            "time_to_complete",
            "is_public",
        )

    def validate(self, attrs):

        data = {}

        if self.instance:
            for field in (
                "place",
                "time",
                "action",
                "is_pleasant",
                "related_habit",
                "period",
                "reward",
                "time_to_complete",
                "is_public",
            ):
                if hasattr(self.instance, field):
                    data[field] = getattr(self.instance, field)

        data.update(attrs)

        data["owner"] = self.context["request"].user

        HabitBusinessValidator()(data)

        return attrs
