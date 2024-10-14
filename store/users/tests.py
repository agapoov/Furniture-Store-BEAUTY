from datetime import timedelta
from http import HTTPStatus
from unittest import mock

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import EmailVerification, User


class UserRegistrationTests(TestCase):

    def setUp(self):
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
        """Testing the correct page display"""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_registration_post_success(self):
        """Testing the successful creation of a user"""
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)


class EmailVerificationTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )

        self.email_verification = EmailVerification.objects.create(user=self.user)

    def test_email_verification_creation(self):
        """Test for the correct creation of the EmailVerification object"""
        self.assertIsNotNone(self.email_verification.code)
        self.assertEqual(self.email_verification.user, self.user)

    @mock.patch('users.models.send_mail')
    def test_send_verification_email(self, mock_send_mail):
        """Testing of sending a verification letter"""
        self.email_verification.send_verification_email()

        self.assertTrue(mock_send_mail.called)

        subject = f'Подтверждение учетной записи для {self.user.username}'
        self.assertEqual(mock_send_mail.call_args[1]['subject'], subject)
        self.assertEqual(mock_send_mail.call_args[1]['recipient_list'], [self.user.email])

    def test_is_expired(self):
        """Expiration Testing"""
        self.assertFalse(self.email_verification.is_expired())

        self.email_verification.expiration = timezone.now() - timedelta(days=1)
        self.assertTrue(self.email_verification.is_expired())

    def test_is_expired_with_custom_duration(self):
        """A test to test the is_expired method with a custom duration"""
        duration = timedelta(hours=1)
        self.assertFalse(self.email_verification.is_expired(duration=duration))

        self.email_verification.created = timezone.now() - timedelta(hours=2)
        self.assertTrue(self.email_verification.is_expired(duration=duration))

    def test_verify_email(self):
        self.assertFalse(self.user.email_is_verified)

        self.email_verification.verify_email()

        self.user.refresh_from_db()
        self.assertTrue(self.user.email_is_verified)


class UserLogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='JustSimplePassword123'
        )
        self.client.login(username='testuser', password='JustSimplePassword123')

    def test_logout_success(self):
        """Testing Logout function"""
        response = self.client.post(reverse('users:logout'))
        self.assertRedirects(response, reverse('main:index'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), f'{self.user.username}, Вы успешно вышли из аккаунта', )
        self.assertNotIn('_auth_user_id', self.client.session)


class UserProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='first_name',
            last_name='last_name',
            username='testuser',
            email='testuser@example.com',
            password='JustSimplePassword123'
        )
        self.url = reverse('users:profile')
        self.client.login(username='testuser', password='JustSimplePassword123')

    def test_update_user_profile_success(self):
        """Testing update_user_profile function"""
        response = self.client.post(self.url, {
            'username': 'testuser_modified',
            'last_name': 'last_name_modified',
            'first_name': 'Vitaliy',
            'email': 'vitaliy@example.com'
        })

        expected_url = reverse('users:profile')
        self.assertRedirects(response, expected_url)

        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'Профиль успешно обновлен')

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'testuser_modified')
        self.assertEqual(self.user.last_name, 'last_name_modified')
        self.assertEqual(self.user.first_name, 'Vitaliy')
        self.assertEqual(self.user.email, 'vitaliy@example.com')

    def test_update_user_profile_error(self):
        """Testing errors when updating"""
        response = self.client.post(self.url, {
            'username': ''
        })
        self.assertEqual(response.status_code, HTTPStatus.OK)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), 'Произошла ошибка')
        self.assertNotEqual(self.user.username, '')
