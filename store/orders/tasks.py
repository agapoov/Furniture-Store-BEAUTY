from celery import shared_task


@shared_task
def send_order_status_email_task(order_id):
    from .models import Order

    try:
        order = Order.objects.get(id=order_id)

        order.send_order_status_email()
    except Order.DoesNotExist:
        pass  # TODO (do error handling)
