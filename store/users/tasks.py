import uuid
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from users.models import User, EmailVerification


@shared_task
def send_verification_email_task(user_id):
    user = User.objects.get(id=user_id)

    expiration_time = now() + timedelta(hours=24)
    email_verification = EmailVerification.objects.create(
        user=user,
        code=uuid.uuid4(),
        expiration=expiration_time
    )
    email_verification.send_verification_email()
