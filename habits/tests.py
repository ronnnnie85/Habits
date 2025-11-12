from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from habits.validators import (HabitBusinessValidator,
                               MaxDurationValueValidator, PeriodValueValidator)

User = get_user_model()


class HabitValidatorsTests(APITestCase):
    def test_max_duration_value_validator_raises_error(self):
        validator = MaxDurationValueValidator(max_seconds=120)
        with self.assertRaises(ValidationError):
            validator(121)

    def test_period_value_validator_raises_error(self):
        validator = PeriodValueValidator(min_days=1, max_days=7)
        with self.assertRaises(ValidationError):
            validator(0)
        with self.assertRaises(ValidationError):
            validator(8)

    def test_business_validator_reward_and_related_forbidden(self):
        user = User.objects.create_user(email="user@example.com", password="pass12345")
        pleasant_habit = Habit.objects.create(
            owner=user,
            place="дом",
            time="21:00",
            action="Принять ванну",
            is_pleasant=True,
            period=1,
            time_to_complete=60,
        )

        data = {
            "reward": "десерт",
            "related_habit": pleasant_habit,
            "is_pleasant": False,
        }
        validator = HabitBusinessValidator()
        with self.assertRaises(ValidationError):
            validator(data)

    def test_business_validator_related_must_be_pleasant(self):
        user = User.objects.create_user(email="user2@example.com", password="pass12345")
        not_pleasant = Habit.objects.create(
            owner=user,
            place="офис",
            time="10:00",
            action="Работать",
            is_pleasant=False,
            period=1,
            time_to_complete=60,
        )
        data = {
            "related_habit": not_pleasant,
            "reward": None,
            "is_pleasant": False,
        }
        validator = HabitBusinessValidator()
        with self.assertRaises(ValidationError):
            validator(data)

    def test_business_validator_pleasant_cannot_have_reward_or_related(self):
        user = User.objects.create_user(email="user3@example.com", password="pass12345")
        pleasant_habit = Habit.objects.create(
            owner=user,
            place="дом",
            time="21:00",
            action="Отдыхать",
            is_pleasant=True,
            period=1,
            time_to_complete=60,
        )

        validator = HabitBusinessValidator()

        data_with_reward = {
            "is_pleasant": True,
            "reward": "кофе",
            "related_habit": None,
        }
        with self.assertRaises(ValidationError):
            validator(data_with_reward)

        data_with_related = {
            "is_pleasant": True,
            "reward": None,
            "related_habit": pleasant_habit,
        }
        with self.assertRaises(ValidationError):
            validator(data_with_related)


class HabitAPITests(APITestCase):
    def setUp(self):
        self.password = "password123"
        self.user = User.objects.create_user(
            email="user@example.com",
            password=self.password,
        )
        self.other_user = User.objects.create_user(
            email="other@example.com",
            password=self.password,
        )

    def authenticate(self, user=None):
        if user is None:
            user = self.user
        url = reverse("users:token_obtain_pair")
        response = self.client.post(
            url, {"email": user.email, "password": self.password}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    def test_create_habit_success(self):
        self.authenticate()
        url = reverse("habits:habit-list")
        data = {
            "place": "дом",
            "time": "09:00",
            "action": "Читать книгу",
            "is_pleasant": False,
            "period": 1,
            "time_to_complete": 60,
            "is_public": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        habit = Habit.objects.first()
        self.assertEqual(habit.action, "Читать книгу")
        self.assertEqual(habit.owner, self.user)

    def test_create_habit_invalid_time_to_complete(self):
        self.authenticate()
        url = reverse("habits:habit-list")
        data = {
            "place": "дом",
            "time": "09:00",
            "action": "Читать",
            "is_pleasant": False,
            "period": 1,
            "time_to_complete": 121,  # нарушаем правило <= 120
            "is_public": False,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_only_owner_can_access_habit(self):
        # создаём привычку от имени user
        habit = Habit.objects.create(
            owner=self.user,
            place="улица",
            time="08:00",
            action="Пробежка",
            is_pleasant=False,
            period=1,
            time_to_complete=60,
            is_public=False,
        )

        # авторизуемся другим пользователем
        self.authenticate(user=self.other_user)
        url = reverse("habits:habit-detail", args=[habit.id])
        response = self.client.get(url)
        # в зависимости от твоей реализации разрешений может быть 403 или 404
        self.assertIn(
            response.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND)
        )

    def test_public_habits_list(self):
        Habit.objects.create(
            owner=self.user,
            place="дом",
            time="09:00",
            action="Читать книгу",
            is_pleasant=False,
            period=1,
            time_to_complete=60,
            is_public=True,
        )
        Habit.objects.create(
            owner=self.user,
            place="офис",
            time="10:00",
            action="Работать",
            is_pleasant=False,
            period=1,
            time_to_complete=60,
            is_public=False,
        )

        url = reverse("habits:public-habits")
        response = self.client.get(url)  # без авторизации, AllowAny
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertTrue(response.data["results"][0]["is_public"])

    def test_habits_pagination(self):
        self.authenticate()
        # создаём 7 привычек
        for i in range(7):
            Habit.objects.create(
                owner=self.user,
                place=f"место {i}",
                time="09:00",
                action=f"действие {i}",
                is_pleasant=False,
                period=1,
                time_to_complete=60,
                is_public=False,
            )

        url = reverse("habits:habit-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        # в settings.PAGE_SIZE = 5
        self.assertEqual(len(response.data["results"]), 5)
        self.assertEqual(response.data["count"], 7)
