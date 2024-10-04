from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import handler404
from store import settings
from store.settings import DEBUG

handler404 = 'main.views.page_not_found'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('catalog/', include('goods.urls', namespace='catalog')),
    path('user/', include('users.urls', namespace='user')),
    path('cart/', include('carts.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('auth/', include('social_django.urls', namespace='social')),
]

if DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
