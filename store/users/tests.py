from datetime import timedelta
from unittest import mock

from django.test import TestCase
from django.utils import timezone

from .models import EmailVerification, User
from django.urls import reverse
from http import HTTPStatus


class UserRegistrationTests(TestCase):

    def setUp(self):
        # Создание тестового пользователя
        self.data = {
            'first_name': 'Vitaliy',
            'last_name': 'Nalivkin',
            'username': 'SimpleUser',
            'email': 'exampleemail@gmail.com',
            'password1': 'UserPassword0987',
            'password2': 'UserPassword0987'
        }
        self.path = reverse('users:registration')

    def test_user_registration_get(self):
        """Тест корректного отображение страницы"""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_registration_post_success(self):
        """Тест успешного создания пользователя"""
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)


class EmailVerificationTest(TestCase):

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )

        # создаем объект EmailVerification
        self.email_verification = EmailVerification.objects.create(user=self.user)

    def test_email_verification_creation(self):
        """Тест корректного создания объекта EmailVerification"""
        self.assertIsNotNone(self.email_verification.code)
        self.assertEqual(self.email_verification.user, self.user)

    @mock.patch('users.models.send_mail')
    def test_send_verification_email(self, mock_send_mail):
        """Тест отправки верификационного письма"""
        self.email_verification.send_verification_email()

        self.assertTrue(mock_send_mail.called)

        subject = f'Подтверждение учетной записи для {self.user.username}'
        self.assertEqual(mock_send_mail.call_args[1]['subject'], subject)
        self.assertEqual(mock_send_mail.call_args[1]['recipient_list'], [self.user.email])

    def test_is_expired(self):
        """Тест истечения срока действия"""
        self.assertFalse(self.email_verification.is_expired())

        # принудительно устаревшая ссылка
        self.email_verification.expiration = timezone.now() - timedelta(days=1)
        self.assertTrue(self.email_verification.is_expired())

    def test_is_expired_with_custom_duration(self):
        """Тест для проверки метода is_expired с кастомной длительностью"""
        duration = timedelta(hours=1)
        self.assertFalse(self.email_verification.is_expired(duration=duration))

        # принудительно устаревший объект
        self.email_verification.created = timezone.now() - timedelta(hours=2)
        self.assertTrue(self.email_verification.is_expired(duration=duration))

    def test_verify_email(self):
        self.assertFalse(self.user.email_is_verified)

        self.email_verification.verify_email()

        self.user.refresh_from_db()
        self.assertTrue(self.user.email_is_verified)
