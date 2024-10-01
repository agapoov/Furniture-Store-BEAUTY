from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('create-order/', views.CreateOrderView.as_view(), name='create-order'),
    path('webhook/yandex_payment/', views.YandexPaymentWebhookView.as_view(), name='yandex_payment_webhook'),
]
