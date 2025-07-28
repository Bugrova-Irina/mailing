from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Модель пользователя"""

    username = None
    email = models.EmailField(
        unique=True,
        verbose_name=_("Email"),
    )
    phone = models.CharField(
        max_length=15,
        verbose_name=_("Телефон"),
        blank=True,
        null=True,
        help_text=_("Введите номер телефона (не обязательно)"),
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name=_("Аватар"),
        blank=True,
        null=True,
        help_text=_("Загрузите изображение для аватара"),
    )
    country = models.CharField(
        max_length=100,
        verbose_name=_("Страна проживания"),
        blank=True,
        null=True,
        help_text=_("Укажите страну проживания"),
    )
    token = models.CharField(
        max_length=100,
        verbose_name=_("Токен"),
        blank=True,
        null=True,
        help_text=_("Токен для верификации"),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
        permissions = [
            ('can_disable_user', _('Can disable user')),
        ]

    def __str__(self):
        return self.email
