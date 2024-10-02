from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('users-cart/', views.UserCartView.as_view(), name='users-cart'),
    path('verify-email/<str:email>/<uuid:code>/', views.EmailVerificationView.as_view(), name='email_verification'),
    path('send-verification-email/', views.EmailVerificationView.as_view(), name='send_verification_email'),
    path('logout/', views.logout, name='logout'),
]
