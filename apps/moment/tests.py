from io import BytesIO
from unittest.mock import PropertyMock, patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image

from apps.moment.forms import MomentForm
from apps.moment.models import Moment

User = get_user_model()


def make_test_image(
    name="test.jpg",
    size=(500, 500),
    image_format="JPEG",
    color="red",
    content_type="image/jpeg",
):
    buffer = BytesIO()
    image = Image.new("RGB", size, color=color)
    image.save(buffer, format=image_format)
    buffer.seek(0)

    return SimpleUploadedFile(
        name=name,
        content=buffer.getvalue(),
        content_type=content_type,
    )


class MomentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="testpass123")
        self.moment = Moment.objects.create(
            owner=self.user, title="Мой момент", details="Какой-то текст"
        )

        self.fake_user = User.objects.create_user(
            username="fake_alice", password="fake_testpass123"
        )
        self.public_moment = Moment.objects.create(
            owner=self.user,
            title="Мой публичный момент",
            details="Какой-то текст",
            is_public=True,
        )

    def test_home_not_authenticated(self):
        response = self.client.get(reverse("moment:home"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Мой момент")
        self.assertContains(response, "Мой публичный момент")

    def test_moment_list_page_status_code(self):
        self.client.login(username="alice", password="testpass123")
        response = self.client.get(reverse("moment:home"))
        self.assertEqual(response.status_code, 200)

    def test_moment_details_page_status_code(self):
        self.client.login(username="alice", password="testpass123")
        response = self.client.get(
            reverse("moment:moment_detail", kwargs={"pk": self.moment.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_moment_details_page_status_code_without_permission(self):
        self.client.login(username="fake_alice", password="fake_testpass123")
        response = self.client.get(
            reverse("moment:moment_detail", kwargs={"pk": self.moment.pk})
        )
        self.assertEqual(response.status_code, 404)

    def test_create_moment(self):
        self.client.login(username="alice", password="testpass123")
        response = self.client.post(
            reverse("moment:create"),
            {
                "title": "Новый момент",
                "details": "Новый текст",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Moment.objects.filter(title="Новый момент").exists())

        moment = Moment.objects.get(title="Новый момент")
        self.assertEqual(str(moment), "Новый момент")

    def test_create_blank_moment(self):
        self.client.login(username="alice", password="testpass123")
        moments_count = Moment.objects.count()

        response = self.client.post(
            reverse("moment:create"),
            {
                "title": "Новый момент",
                "details": "",
                "music": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Момент не может быть пустым (заполните одно из: описание/изображение/музыка)",
        )
        self.assertFalse(Moment.objects.filter(title="Новый момент").exists())
        self.assertEqual(Moment.objects.count(), moments_count)

    def test_list_moment(self):
        self.client.login(username="alice", password="testpass123")
        response = self.client.get(reverse("moment:self_moments_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Мой момент")
        self.assertContains(response, "Мой публичный момент")

    def test_list_moment_is_public(self):
        self.client.login(username="fake_alice", password="fake_testpass123")
        response = self.client.get(reverse("moment:public_moments_list"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Мой момент")
        self.assertContains(response, "Мой публичный момент")

    def test_update_moment(self):
        self.client.login(username="alice", password="testpass123")
        response = self.client.post(
            reverse("moment:moment_update", kwargs={"pk": self.moment.pk}),
            {
                "title": "Обновленный момент",
                "details": "Измененный текст",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.moment.refresh_from_db()
        self.assertEqual(self.moment.title, "Обновленный момент")

    def test_update_moment_without_permission(self):
        self.client.login(username="fake_alice", password="fake_testpass123")
        response = self.client.post(
            reverse("moment:moment_update", kwargs={"pk": self.moment.pk}),
            {
                "title": "Обновленный момент",
                "details": "Измененный текст",
            },
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_moment(self):
        self.client.login(username="alice", password="testpass123")
        response = self.client.post(
            reverse("moment:moment_delete", kwargs={"pk": self.moment.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Moment.objects.filter(pk=self.moment.pk).exists())

    def test_delete_moment_without_permission(self):
        self.client.login(username="fake_alice", password="fake_testpass123")
        response = self.client.post(
            reverse("moment:moment_delete", kwargs={"pk": self.moment.pk})
        )
        self.assertEqual(response.status_code, 404)

    def test_search_field(self):
        self.client.login(username="alice", password="testpass123")
        response = self.client.get(reverse("moment:search"), {"q": "пуб"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Мой момент")
        self.assertContains(response, "Мой публичный момент")

    def test_search_field_if_none(self):
        self.client.login(username="alice", password="")
        response = self.client.get(reverse("moment:search"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["moments"]), 0)

    def test_clean_image_accepts_valid_image(self):
        image = make_test_image(size=(800, 800))

        form = MomentForm(
            data={"title": "Тест", "details": "Описание"}, files={"image": image}
        )

        self.assertTrue(form.is_valid(), form.errors)
        cleaned_image = form.cleaned_data["image"]

        self.assertTrue(cleaned_image.name.endswith(".jpg"))
        self.assertEqual(cleaned_image.content_type, "image/jpeg")

    def test_clean_image_resizes_large_image(self):
        image = make_test_image(name="big.jpg", size=(3000, 2000))

        form = MomentForm(
            data={"title": "Тест", "details": "Описание"}, files={"image": image}
        )

        self.assertTrue(form.is_valid(), form.errors)

        cleaned_image = form.cleaned_data["image"]
        cleaned_image.seek(0)

        img = Image.open(cleaned_image)
        self.assertLessEqual(max(img.size), 1600)

    def test_clean_image_rejects_small_image(self):
        image = make_test_image(size=(300, 300))

        form = MomentForm(
            data={"title": "Тест", "details": "Описание"}, files={"image": image}
        )

        self.assertFalse(form.is_valid())
        self.assertIn("image", form.errors)
        self.assertIn("Картинка слишком маленькая", form.errors["image"][0])

    def test_clean_image_rejects_invalid_image_file(self):
        image = SimpleUploadedFile(
            "fake.jpg",
            b"not really an image",
            content_type="image/jpeg",
        )

        form = MomentForm(
            data={"title": "Тест", "details": "Описание"}, files={"image": image}
        )

        self.assertFalse(form.is_valid())
        self.assertIn("image", form.errors)
        self.assertIn("Upload a valid image", form.errors["image"][0])

    def test_clean_image_resizes_large_wight(self):
        image = make_test_image(size=(1000, 1000))

        with patch.object(type(image), "size", new_callable=PropertyMock) as mock_size:
            mock_size.return_value = 11 * 1024 * 1024

            form = MomentForm(
                data={"title": "Тест", "details": "Описание"},
                files={"image": image},
            )

            self.assertFalse(form.is_valid())
            self.assertIn("Картинка слишком большая", form.errors["image"][0])

    def test_clean_image_rejects_too_large_dimensions(self):
        image = make_test_image(size=(9001, 400))

        form = MomentForm(
            data={"title": "Тест", "details": "Описание"},
            files={"image": image},
        )

        self.assertFalse(form.is_valid())
        self.assertIn("image", form.errors)
        self.assertIn("Изображение слишком большое", form.errors["image"][0])
