import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser, send_mail
from django.db import models
from django.urls import reverse
from django.utils import timezone


class User(AbstractUser):
    image = models.ImageField(upload_to='users/images', null=True, blank=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    email_is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username


class EmailVerification(models.Model):
    code = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(default=timezone.now() + timedelta(days=1))

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = ('Для подтверждения учетной записи с почтой {} перейдите по ссылке: {} '
                   'С уважением, команда BEAUTY').format(
            self.user.email,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self, duration=None):
        """Проверка истечения срока действия ссылки или времени для отправки нового письма"""
        if duration:
            return timezone.now() >= self.created + duration
        return timezone.now() >= self.expiration

    def verify_email(self):
        """Подтверждение электронной почты у пользователя"""
        self.user.email_is_verified = True
        self.user.save()
