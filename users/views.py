import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import ManagerForm, UserForm, UserRegisterForm
from users.models import User


class UserDetailView(DetailView):
    """Класс для просмотра профиля пользователя"""

    model = User
    template_name = "users/profile.html"
    context_object_name = "profile_user"


class UserListView(LoginRequiredMixin, ListView):
    """Класс для просмотра списка пользователей"""

    model = User
    template_name = "users/users_list.html"
    context_object_name = "users"

    def get_queryset(self):
        """
        Менеджеры видят всех пользователей, обычные пользователи - только свой профиль
        """

        if self.request.user.is_superuser:
            return User.objects.all()
        if self.request.user.has_perm("users.can_disable_user"):
            return User.objects.all()  # Менеджер видит всех
        # Пользователь - только свой профиль
        return User.objects.filter(pk=self.request.user.pk)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Класс для редактирования информации о пользователе"""

    model = User

    def get_object(self, queryset=None):
        user = self.request.user
        target_user = get_object_or_404(User, pk=self.kwargs["pk"])

        # Разрешаем доступ, если:
        # 1. Пользователь - суперпользователь
        # 2. Пользователь - менеджер (с правом can_disable_user)
        # 3. Пользователь редактирует свой собственный профиль
        if (
            user.is_superuser
            or user.has_perm("users.can_disable_user")
            or user.pk == target_user.pk
        ):
            return target_user
        raise PermissionDenied("У вас нет прав для редактирования этого профиля")

    def get_form_class(self):
        user = self.request.user
        # Получаем пользователя, которого редактируем
        target_user = self.get_object()
        # Если менеджер редактирует не свой профиль
        if user.has_perm("users.can_disable_user") and user.pk != target_user.pk:
            return ManagerForm
        # Во всех остальных случаях свой профиль или обычный пользователь
        return UserForm

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
