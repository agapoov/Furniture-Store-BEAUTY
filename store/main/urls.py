from django.urls import path
from django.views.decorators.cache import cache_page

from .views import AboutView, ContactView, DeliveryView, HomeView

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('about/', cache_page(60)(AboutView.as_view()), name='about'),
    path('delivery_details/', DeliveryView.as_view(), name='delivery_details'),
    path('contact/', ContactView.as_view(), name='contact'),

]
