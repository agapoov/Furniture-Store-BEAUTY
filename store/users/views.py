import uuid
from datetime import timedelta

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views.generic import CreateView, TemplateView, UpdateView, View

from carts.models import Cart
from common.mixins import CacheMixin
from orders.models import Order, OrderItem
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm

from .models import EmailVerification


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('users:logout'):
            return redirect_page
        return reverse_lazy('main:index')

    def form_valid(self, form):
        session_key = self.request.session.session_key

        user = form.get_user()
        if user:
            auth.login(self.request, user)
            if session_key:
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                Cart.objects.filter(session_key=session_key).update(user=user)

                messages.success(self.request, f'{user.first_name}, Вы успешно вошли в аккаунт.')

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'BEAUTY - Авторизация'
        return context


class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        user = form.save()  # Now sending verification mail here

        auth.login(self.request, user)

        # Updating cart
        session_key = self.request.session.session_key
        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)

        messages.success(self.request, f'{user.first_name}, вы успешно зарегистрировались. '
                                       'Пожалуйста, подтвердите свою почту.')

        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'BEAUTY - Регистрация'
        return context


class EmailVerificationView(View):
    @staticmethod
    def get(request, email, code):
        verification = get_object_or_404(EmailVerification, user__email=email, code=code)

        if not verification.is_expired():
            verification.verify_email()
            messages.success(request, 'Ваш email успешно подтвержден!')
        else:
            messages.warning(request, 'Ссылка для подтверждения почты истекла.')

        return redirect('users:profile')

    @staticmethod
    def post(request):
        user = request.user
        verification = EmailVerification.objects.filter(user=user).first()

        if verification and not verification.is_expired():
            messages.warning(request, 'Вы можете отправить новое письмо с подтверждением только через 24 часа.')
        else:
            if verification:
                verification.delete()  # удаляем старую запись, если она есть
            verification = EmailVerification.objects.create(user=user)
            verification.send_verification_email()
            messages.success(request, 'Письмо с подтверждением было отправлено на ваш email.')

        return redirect('users:profile')


class UserProfileView(LoginRequiredMixin, CacheMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Произошла ошибка')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'BEAUTY - Профиль'

        orders = Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch('orderitem_set',
                     queryset=OrderItem.objects.select_related('product'),
                     )
        ).order_by('-id')
        context['orders'] = self.set_get_cache(orders, f'user {self.request.user} orders', 3)
        return context


class UserCartView(TemplateView):
    template_name = 'users/users_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'BEAUTY - Корзина'
        return context


@login_required
def logout(request):
    messages.success(request, f'{request.user.username}, Вы успешно вышли из аккаунта')
    auth.logout(request)
    return redirect(reverse('main:index'))
