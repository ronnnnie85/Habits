from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserTests(APITestCase):
    def setUp(self):
        self.password = "testpassword123"
        self.user = User.objects.create_user(
            email="user@example.com",
            password=self.password,
            phone="1234567890",
        )

    def authenticate(self):
        """Получить access-токен и прописать его в заголовки клиента."""
        url = reverse("users:token_obtain_pair")
        response = self.client.post(
            url, {"email": self.user.email, "password": self.password}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    def test_registration_creates_user(self):
        url = reverse("users:register")
        data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
            "phone": "79991234567",
            "tg_id": "123456789",
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_obtain_jwt_token(self):
        url = reverse("users:token_obtain_pair")
        data = {
            "email": self.user.email,
            "password": self.password,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_profile_get(self):
        self.authenticate()
        url = reverse("users:user_profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_profile_update_tg_id(self):
        self.authenticate()
        url = reverse("users:user_profile")
        data = {"tg_id": "999999999", "phone": "70000000000"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.tg_id, "999999999")
        self.assertEqual(self.user.phone, "70000000000")