from django.urls import path

from .views import AboutView, HomeView

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about')
]