from django.db import models

class MailingListRecipient(models.Model):
    """Получатель рассылки"""
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Введите адрес электронной почты",
    )
    recipient_name = models.CharField(
        max_length=350,
        verbose_name="ФИО",
        help_text="Введите Ваши фамилию, имя, отчество",
    )
    comment = models.TextField(
        verbose_name="Комментарий",
        help_text="Оставьте свой комментарий",
        blank=True,
        null=True,
    )
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='Группы пользователей',
        related_name='custom_user_groups',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permission',
        blank=True,
        help_text='Особые права для пользователя',
        related_name='custom_user_permissions',
        related_query_name='user',
    )

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"

    def __str__(self):
        return f"{self.recipient_name}, {self.email}"


class Letter(models.Model):
    """Письмо для рассылки"""
    title = models.CharField(
        max_length=300,
        verbose_name="Тема письма",
        help_text="Введите тему письма",
    )
    description = models.TextField(
        verbose_name="Содержимое письма",
        help_text="Добавьте содержимое письма",
    )

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"

    def __str__(self):
        return self.title


class Mailing(models.Model):
    """Рассылка"""
    # Статусы рассылки
    CREATED = 'created'
    STARTED = 'started'
    COMPLETED = 'completed'
    STATUS_CHOICES = [
        (CREATED, 'Создана'),
        (STARTED, 'Запущена'),
        (COMPLETED, 'Завершена'),
    ]

    start_sending = models.DateTimeField(
        verbose_name="Дата старта рассылки",
        help_text="Укажите дату старта рассылки",
    )
    end_sending = models.DateTimeField(
        verbose_name="Дата окончания рассылки",
        help_text="Укажите дату окончания рассылки",
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=CREATED,
        verbose_name="Статус",
        help_text="Статус рассылки",
    )
    letter = models.ForeignKey(
        Letter,
        on_delete=models.SET_NULL,
        verbose_name="Письмо",
        help_text="Выберите письмо для рассылки",
        blank=True,
        null=True,
        related_name="mailings",
    )
    recipients = models.ManyToManyField(
        MailingListRecipient,
        verbose_name="Получатель",
        help_text="Введите получателей рассылки",
    )

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"

    def get_letter_title(self):
        """Получение темы письма с обработкой null"""
        return self.letter.title if self.letter else "Без темы"

    def __str__(self):
        # если тема письма не указана, установить значение "Без темы"
        return f"Рассылка '{self.get_letter_title()}', статус: '{self.get_status_display()}'"


class AttemptToSend(models.Model):
    """Попытка рассылки"""
    # Статусы попытки
    SUCCESS = 'success'
    FAILED = 'failed'
    STATUS_CHOICES = [
        (SUCCESS, 'Успешно'),
        (FAILED, 'Не успешно'),
    ]

    attempt_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата попытки",
        help_text="Дата и время попытки отправки",
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        verbose_name="Статус попытки",
        help_text="Результат попытки отправки",
    )
    mail_server_response = models.TextField(
        verbose_name="Ответ от сервера",
        help_text="Ответ почтового сервера",
        blank=True,
        null=True,
    )
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        verbose_name="Рассылка",
        related_name="attempts",
    )

    class Meta:
        verbose_name = "попытка рассылки"
        verbose_name_plural = "попытки рассылки"
        ordering = ['-attempt_date'] # Сортировка по умолчанию

    def __str__(self):
        return (f"Попытка рассылки: {self.mailing}, "
                f"дата: {self.attempt_date.strftime('%Y-%m-%d %H:%M')}, "
                f"статус: {self.get_status_display()}")
