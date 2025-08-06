from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from config.settings import EMAIL_HOST_USER
from mailings.forms import (
    AttemptCreateForm,
    LetterCreateForm,
    MailingCreateForm,
    MailingManagerUpdateForm,
    RecipientsCreateForm,
)
from mailings.models import AttemptToSend, Letter, Mailing, Recipients


class MainPageView(DetailView):
    """Класс для отображения главной страницы"""

    template_name = "mailings/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем статистику
        context["total_mailings"] = Mailing.objects.count()
        context["active_mailings"] = Mailing.objects.filter(
            status=Mailing.STARTED
        ).count()
        context["unique_recipients"] = Recipients.objects.count()
        return context

    def get_object(self, queryset=None):
        # Возвращаем None, так как нам не нужен конкретный объект для отображения
        return None


class RecipientsListView(LoginRequiredMixin, ListView):
    """Список всех получателей"""

    model = Recipients
    template_name = "mailings/recipients_list.html"
    context_object_name = "recipients"

    def get_queryset(self):
        """
        Менеджеры видят всех клиентов, пользователи - только тех,
        которых создали сами
        """
        from .services import get_cached_recipients

        return get_cached_recipients(self.request.user)


class RecipientsDetailView(DetailView):
    """Просмотр данных получателя"""

    model = Recipients
    template_name = "mailings/recipients_detail.html"
    context_object_name = "recipient"


class RecipientsCreateView(LoginRequiredMixin, CreateView):
    """Добавление нового получателя"""

    model = Recipients
    form_class = RecipientsCreateForm
    template_name = "mailings/recipient_form.html"
    success_url = reverse_lazy("mailings:recipients_list")

    def form_valid(self, form):
        """
        Автоматически назначаем владельцем получателя пользователя,
        создавшего получателя
        """
        recipient = form.save()
        user = self.request.user
        recipient.owner = user
        recipient.save()
        return super().form_valid(form)


class RecipientsUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование данных получателя"""

    model = Recipients
    form_class = RecipientsCreateForm
    template_name = "mailings/recipient_form.html"
    success_url = reverse_lazy("mailings:recipients_list")

    def get_form_class(self):
        recipient = self.get_object()  # Получаем текущего пользователя
        user = self.request.user

        # если авторизован владелец клиента, он может его редактировать
        if recipient.owner == user:
            return RecipientsCreateForm

    def get_success_url(
        self,
    ):  # перенаправление на просмотр отредактированного получателя
        return reverse("mailings:recipient_detail", args=[self.kwargs.get("pk")])


class RecipientsDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление получателя"""

    model = Recipients
    template_name = "mailings/recipient_confirm_delete.html"
    success_url = reverse_lazy("mailings:recipients_list")

    def get_queryset(self):
        """Ограничиваем доступ - удалять можно только своих клиентов"""
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(owner=self.request.user)


class LetterListView(LoginRequiredMixin, ListView):
    """Список всех сообщений"""

    model = Letter
    template_name = "mailings/letters_list.html"
    context_object_name = "letters"

    def get_queryset(self):
        """
        Менеджеры видят все письма, пользователи - только те,
        которые создали сами
        """
        from .services import get_cached_letters

        return get_cached_letters(self.request.user)


class LetterDetailView(DetailView):
    """Просмотр письма"""

    model = Letter
    template_name = "mailings/letter_detail.html"
    context_object_name = "letter"


class LetterCreateView(LoginRequiredMixin, CreateView):
    """Создание нового письма"""

    model = Letter
    form_class = LetterCreateForm
    template_name = "mailings/letter_form.html"
    success_url = reverse_lazy("mailings:letters_list")

    def form_valid(self, form):
        """
        Автоматически назначаем владельцем письма пользователя,
        создавшего письмо
        """
        letter = form.save()
        user = self.request.user
        letter.owner = user
        letter.save()
        return super().form_valid(form)


class LetterUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование письма"""

    model = Letter
    form_class = LetterCreateForm
    template_name = "mailings/letter_form.html"
    success_url = reverse_lazy("mailings:letters_list")

    def get_form_class(self):
        letter = self.get_object()  # получаем текущее письмо
        user = self.request.user

        # если владелец письма, он может редактировать письмо
        if letter.owner == user:
            return LetterCreateForm

    def get_success_url(self):  # перенаправление на просмотр отредактированного письма
        return reverse("mailings:letter_detail", args=[self.kwargs.get("pk")])


class LetterDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление письма"""

    model = Letter
    template_name = "mailings/letter_confirm_delete.html"
    success_url = reverse_lazy("mailings:letters_list")

    def get_queryset(self):
        """Ограничиваем доступ - удалять можно только свои письма"""
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(owner=self.request.user)


class MailingListView(LoginRequiredMixin, ListView):
    """Список всех рассылок"""

    model = Mailing
    template_name = "mailings/mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        """
        Менеджеры видят все рассылки, пользователи - только те,
        которые создали сами
        """
        from .services import get_cached_mailings

        return get_cached_mailings(self.request.user)


class MailingDetailView(DetailView):
    """Просмотр рассылки"""

    model = Mailing
    template_name = "mailings/mailing_detail.html"
    context_object_name = "mailing"


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Создание новой рассылки"""

    model = Mailing
    form_class = MailingCreateForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def form_valid(self, form):
        """
        Автоматически назначаем владельцем рассылки пользователя,
        создавшего рассылку
        """
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование рассылки"""

    model = Mailing
    form_class = MailingCreateForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_form_class(self):
        mailing = self.get_object()  # получаем текущую рассылку
        user = self.request.user

        # если авторизован менеджер и он не владелец рассылки,
        # загружается форма для изменения статуса рассылки
        if (
            user.has_perm("users.can_disable_user")
            and not user.is_superuser
            and mailing.owner != user
        ):
            return MailingManagerUpdateForm
        return MailingCreateForm

    def get_success_url(self):  # перенаправление на просмотр отредактированной рассылки
        return reverse("mailings:mailing_detail", args=[self.kwargs.get("pk")])


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление рассылки"""

    model = Mailing
    template_name = "mailings/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_queryset(self):
        """Ограничиваем доступ - удалять можно только свои рассылки"""
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(owner=self.request.user)


class AttemptToSendCreateView(LoginRequiredMixin, CreateView):
    """Запуск попытки отправки рассылки"""

    model = AttemptToSend
    form_class = AttemptCreateForm
    template_name = "mailings/attempt_form.html"
    success_url = reverse_lazy("mailings:attempts_list")

    def form_valid(self, form):
        # создаем объект попытки, но пока не сохраняем
        attempt = form.save(commit=False)
        mailing = attempt.mailing

        # Устанавливаем владельца попытки
        attempt.owner = self.request.user

        # Получаем содержимое письма
        message = mailing.letter.description if mailing.letter else ""
        subject = mailing.letter.title if mailing.letter else "Без темы"

        # Получаем список email получателей
        recipients_emails = list(mailing.recipients.values_list("email", flat=True))
        total_recipients = len(recipients_emails)  # Сохраняем количество получателей

        # Сохраняем количество получателей до попытки рассылки
        attempt.emails_sent = total_recipients

        try:
            # отправка письма
            result = send_mail(
                subject=subject,
                message=message,
                from_email=EMAIL_HOST_USER,
                recipient_list=list(recipients_emails),
                fail_silently=False,
            )

            # Обновляем статус попытки
            attempt.status = AttemptToSend.SUCCESS
            attempt.mail_server_response = (
                f"Успешно отправлено письмо для {total_recipients} получателей"
            )

            # Для успешной отправки количество отправленных сообщений =
            # количеству получателей (result всегда будет = 1, т.к.
            # это один пакет писем

        except Exception as e:
            # Фиксируем ошибку
            attempt.status = AttemptToSend.FAILED
            attempt.mail_server_response = f"Ошибка: {str(e)}"

            # Для неудачной попытки сохраняем количество получателей, которых
            # пытались отправить (уже сохранено выше)

        # Сохраняем попытку с обновленными данными
        attempt.save()
        return super().form_valid(form)


class AttemptToSendListView(LoginRequiredMixin, ListView):
    """Список попыток отправки рассылок"""

    model = AttemptToSend
    template_name = "mailings/attempts_list.html"
    context_object_name = "attempts"

    def get_queryset(self):
        """
        Менеджеры видят все попытки, пользователи - только свои
        """
        from .services import get_cached_attempts

        return get_cached_attempts(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем queryset с учетом фильтрации
        attempts = self.get_queryset()  # Используем кешированный queryset
        # Получаем статистику по отфильтрованным попыткам
        context["success_attempts"] = sum(
            1 for a in attempts if a.status == AttemptToSend.SUCCESS
        )  # Успешные попытки
        context["wrong_attempts"] = sum(
            1 for a in attempts if a.status == AttemptToSend.FAILED
        )  # Неудачные попытки
        # Общее количество отправленных сообщений
        context["total_emails_sent"] = sum(
            a.emails_sent for a in attempts if a.status == AttemptToSend.SUCCESS
        )

        return context


class AttemptToSendDetailView(LoginRequiredMixin, DetailView):
    """Подробная информация о попытке отправки рассылки"""

    model = AttemptToSend
    template_name = "mailings/attempt_detail.html"
    context_object_name = "attempt"

    def dispatch(self, request, *args, **kwargs):
        """
        Проверяем, имеет ли право пользователь просматривать эту попытку
        """
        obj = self.get_object()
        if not (
            request.user.is_superuser
            or request.user.has_perm("users.can_disable_user")
            or obj.owner == request.user
        ):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
