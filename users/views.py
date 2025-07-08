import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserForm, UserRegisterForm
from users.models import User


class UserDetailView(DetailView):
    """Класс для просмотра профиля пользователя"""

    model = User
    template_name = "users/profile.html"
    context_object_name = "user"


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Класс для редактирования информации о пользователе"""

    model = User
    form_class = UserForm

    def get_object(self, queryset=None):
        # Пользователь может редактировать только свой профиль
        return self.request.user

    # после сохранения данных перенаправляем пользователя на страницу профиля
    def get_success_url(self):
        # Динамически формируем url с использованием pk текущего пользователя
        return reverse("users:profile", kwargs={"pk": self.object.pk})


class UserCreateView(CreateView):
    """Класс для создания пользователя"""

    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()  # сохранение результатов заполнения формы
        user.is_active = (
            False  # пользователь создан, но не может авторизоваться на сайте
        )
        token = secrets.token_hex(16)  # токен для пользователя
        user.token = token
        user.save()
        host = self.request.get_host()
        # ссылка для подтверждения регистрации пользователя
        url = f"http://{host}/users/email-confirm/{token}"
        # отправка письма пользователю для подтверждения регистрации
        send_mail(
            subject="Подтверждение почты",
            message=f"Добрый день. Перейдите по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    """
    если пользователь перешел по ссылке из письма,
    он может авторизоваться на сайте
    """
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))
