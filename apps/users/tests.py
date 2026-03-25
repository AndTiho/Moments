from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="testpass123")

    def test_register_user(self):
        response = self.client.post(
            reverse("users:register"),
            {
                "username": "newuser",
                "password1": "StrongPass123",
                "password2": "StrongPass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_profile_page_for_logged_in_user(self):
        self.client.login(username="alice", password="testpass123")
        response = self.client.get(
            reverse("users:profile", kwargs={"pk": self.user.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_update_profile(self):
        self.client.login(username="alice", password="testpass123")
        response = self.client.post(
            reverse("users:update", kwargs={"pk": self.user.pk}),
            {
                "username": "alice_new",
                "email": "alice@example.com",
                "first_name": "Alice",
                "about_me": "Привет",
                "header_name_preference": "username",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "alice_new")

    def test_update_profile_header_name(self):
        self.client.login(username="alice", password="testpass123")
        response = self.client.post(
            reverse("users:update", kwargs={"pk": self.user.pk}),
            {
                "username": "alice_new",
                "email": "alice@example.com",
                "first_name": "Alice",
                "about_me": "Привет",
                "header_name_preference": "name",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.header_display_name, "Alice")


    def test_delete_profile(self):
        self.client.login(username="alice", password="testpass123")
        response = self.client.post(
            reverse("users:confirm_delete", kwargs={"pk": self.user.pk}), {}
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username="alice").exists())
