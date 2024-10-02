from celery import shared_task
from django.core.mail import send_mail

from store.settings import EMAIL_HOST_USER


@shared_task
def send_order_status_email(order_id):
    from .models import Order

    order = Order.objects.get(payment_id=order_id)
    subject = 'Статус вашего заказа'
    message = f'Ваш заказ #{order.id} был обновлён. Новый статус: {order.get_status_display()}.'
    recipient_list = [order.user.email]

    return send_mail(subject, message, EMAIL_HOST_USER, recipient_list)


