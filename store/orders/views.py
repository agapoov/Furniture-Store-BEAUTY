import json
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.urls import reverse
from carts.models import Cart
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
from yookassa import Configuration, Payment
from store.settings import YOOKASSA_SHOP_ID, YOOKASSA_API_KEY


Configuration.account_id = YOOKASSA_SHOP_ID
Configuration.secret_key = YOOKASSA_API_KEY


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('users:profile')

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user
                cart_items = Cart.objects.filter(user=user)

                if cart_items.exists():
                    order = Order.objects.create(
                        user=user,
                        phone_number=form.cleaned_data['phone_number'],
                        requires_delivery=form.cleaned_data['requires_delivery'],
                        delivery_address=form.cleaned_data['delivery_address'],
                        payment_on_get=form.cleaned_data['payment_on_get']
                    )

                    total_price = 0  # Сумма заказа
                    for cart_item in cart_items:
                        product = cart_item.product
                        name = cart_item.product.name
                        price = cart_item.product.sell_price()
                        quantity = cart_item.quantity

                        if product.quantity < quantity:
                            raise ValidationError(f'Недостаточное кол-во товара {name} на складе\n'
                                                  f'В наличии - {product.quantity}')

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            price=price,
                            quantity=quantity,
                        )
                        product.quantity -= quantity
                        product.save()

                        total_price += price * quantity  # Увеличиваем общую сумму

                    cart_items.delete()  # очищаем после создания заказа

                    payment_method = form.cleaned_data['payment_on_get']
                    if payment_method == '0':  # Если оплата картой
                        # Создаем платеж через yookassa
                        payment = Payment.create({
                            "amount": {
                                "value": total_price,
                                "currency": "RUB"
                            },
                            "confirmation": {
                                "type": "redirect",
                                "return_url": self.request.build_absolute_uri(reverse('users:profile'))
                            },
                            "capture": True,
                            "description": f"Оплата заказа #{order.id}"
                        })

                        # Сохраняем ID платежа в заказе
                        order.payment_id = payment.id
                        order.save()

                        # Перенаправление на страницу Юкасси для оплаты
                        return redirect(payment.confirmation.confirmation_url)

                    messages.success(self.request, 'Заказ оформлен')
                    return redirect('users:profile')

        except ValidationError as e:
            messages.warning(self.request, str(e))
            return redirect('orders:create-order')

    def form_invalid(self, form):
        messages.error(self.request, 'Заполните все обязательные поля')
        return redirect('orders:create-order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'BEAUTY - Оформление заказа'
        context['order'] = True
        return context


@method_decorator(csrf_exempt, name='dispatch')
class YandexPaymentWebhookView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        payment_id = data['object']['id']
        status = data['event']

        if status == 'payment.succeeded':
            try:
                order = Order.objects.get(payment_id=payment_id)
                order.is_paid = True
                order.status = 'paid'
                order.save()
                return JsonResponse({'status': 'success'}, status=200)
            except Order.DoesNotExist:
                return JsonResponse({'status': 'order not found'}, status=404)

        elif status == 'payment.canceled':
            try:
                order = Order.objects.get(payment_id=payment_id)
                order.status = 'canceled'
                order.save()
                return JsonResponse({'status': 'order canceled'}, status=200)
            except Order.DoesNotExist:
                return JsonResponse({'status': 'order not found'}, status=404)

        return JsonResponse({'status': 'ignored'}, status=200)