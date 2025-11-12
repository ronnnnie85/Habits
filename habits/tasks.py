from celery import shared_task
from django.utils import timezone

from .models import Habit
from .services import send_telegram_message


@shared_task
def send_habit_reminders():
    now = timezone.localtime()
    current_time = now.time().replace(second=0, microsecond=0)

    habits = Habit.objects.filter(time=current_time)

    for habit in habits:
        user = habit.owner

        if not user.tg_id:
            continue

        text = (
            f"Напоминание о привычке:\n"
            f'{habit.action} в {habit.place} в {habit.time.strftime("%H:%M")}'
        )
        send_telegram_message(user.tg_id, text)
