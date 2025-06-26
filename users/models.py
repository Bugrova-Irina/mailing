from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name='Email',
    )
    phone = models.CharField(
        max_length=15,
        verbose_name='Телефон',
        blank=True,
        null=True,
        help_text='Введите номер телефона (не обязательно)',
    )
    avatar = models.ImageField(
        upload_to='users/avatars',
        verbose_name='Аватар',
        blank=True,
        null=True,
        help_text='Загрузите изображение для аватара',
    )
    country = models.CharField(
        max_length=100,
        verbose_name='Страна проживания',
        blank=True,
        null=True,
        help_text='Укажите страну проживания',
    )
    token = models.CharField(
        max_length=100,
        verbose_name='Токен',
        blank=True,
        null=True,
        help_text='Токен для верификации',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
