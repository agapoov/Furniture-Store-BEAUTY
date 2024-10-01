from django.urls import path
from django.views.decorators.cache import cache_page
from .views import AboutView, HomeView

app_name = 'main'

urlpatterns = [
    path('', cache_page(60)(HomeView.as_view()), name='index'),
    path('about/', cache_page(60)(AboutView.as_view()), name='about')
]
