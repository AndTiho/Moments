from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.moment.models import Moment

User = get_user_model()


class MomentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='alice',
            password='testpass123'
        )
        self.moment = Moment.objects.create(
            owner=self.user,
            title='Мой момент',
            details='Какой-то текст'
        )

        self.fake_user = User.objects.create_user(username='fake_alice', password='fake_testpass123')
        self.public_moment = Moment.objects.create(
            owner=self.user,
            title='Мой публичный момент',
            details='Какой-то текст',
            is_public=True,
        )
    def test_home_not_authenticated(self):
        response = self.client.get(reverse('moment:home'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Мой момент')
        self.assertContains(response, 'Мой публичный момент')

    def test_moment_list_page_status_code(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('moment:home'))
        self.assertEqual(response.status_code, 200)

    def test_moment_details_page_status_code(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('moment:moment_detail', kwargs={'pk': self.moment.pk}))
        self.assertEqual(response.status_code, 200)

    def test_moment_details_page_status_code_without_permission(self):
        self.client.login(username='fake_alice', password='fake_testpass123')
        response = self.client.get(reverse('moment:moment_detail', kwargs={'pk': self.moment.pk}))
        self.assertEqual(response.status_code, 404)

    def test_create_moment(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.post(reverse('moment:create'), {
            'title': 'Новый момент',
            'details': 'Новый текст',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Moment.objects.filter(title='Новый момент').exists())

        moment = Moment.objects.get(title='Новый момент')
        self.assertEqual(str(moment), "Новый момент")

    def test_create_blank_moment(self):
        self.client.login(username='alice', password='testpass123')
        moments_count = Moment.objects.count()

        response = self.client.post(reverse('moment:create'), {
            'title': 'Новый момент',
            'details': '',
            'music': '',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Момент не может быть пустым (заполните одно из: описание/изображение/музыка)'
        )
        self.assertFalse(Moment.objects.filter(title='Новый момент').exists())
        self.assertEqual(Moment.objects.count(), moments_count)

    def test_list_moment(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('moment:self_moments_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Мой момент')
        self.assertContains(response, 'Мой публичный момент')

    def test_list_moment_is_public(self):
        self.client.login(username='fake_alice', password='fake_testpass123')
        response = self.client.get(reverse('moment:public_moments_list'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Мой момент')
        self.assertContains(response, 'Мой публичный момент')

    def test_update_moment(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.post(reverse('moment:moment_update', kwargs={'pk': self.moment.pk}), {
            'title': 'Обновленный момент',
            'details': 'Измененный текст',
        })
        self.assertEqual(response.status_code, 302)
        self.moment.refresh_from_db()
        self.assertEqual(self.moment.title, 'Обновленный момент')

    def test_update_moment_without_permission(self):
        self.client.login(username='fake_alice', password='fake_testpass123')
        response = self.client.post(reverse('moment:moment_update', kwargs={'pk': self.moment.pk}), {
            'title': 'Обновленный момент',
            'details': 'Измененный текст',
        })
        self.assertEqual(response.status_code, 404)

    def test_delete_moment(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.post(reverse('moment:moment_delete', kwargs={'pk': self.moment.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Moment.objects.filter(pk=self.moment.pk).exists())

    def test_delete_moment_without_permission(self):
        self.client.login(username='fake_alice', password='fake_testpass123')
        response = self.client.post(reverse('moment:moment_delete', kwargs={'pk': self.moment.pk}))
        self.assertEqual(response.status_code, 404)

    def test_search_field(self):
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('moment:search'),{'q':'пуб'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Мой момент')
        self.assertContains(response, 'Мой публичный момент')

    def test_search_field_if_none(self):
        self.client.login(username='alice', password='')
        response = self.client.get(reverse('moment:search'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['moments']), 0)