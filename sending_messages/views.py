from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from config.settings import EMAIL_HOST_USER
from sending_messages.forms import MailingCreateForm, LetterCreateForm, RecipientsCreateForm, AttemptCreateForm
from sending_messages.models import MailingListRecipient, Letter, Mailing, AttemptToSend


class MainPageView(DetailView):
    """Класс для отображения главной страницы"""
    template_name = 'sending_messages/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем статистику
        context['total_mailings'] = Mailing.objects.count()
        context['active_mailings'] = Mailing.objects.filter(status=Mailing.STARTED).count()
        context['unique_recipients'] = MailingListRecipient.objects.count()
        return context

    def get_object(self, queryset=None):
        # Возвращаем None, так как нам не нужен конкретный объект для отображения
        return None


class MailingListRecipientListView(ListView):
    """Список всех получателей"""
    model = MailingListRecipient
    template_name = 'sending_messages/recipients_list.html'
    context_object_name = 'recipients'


class MailingListRecipientDetailView(DetailView):
    """Просмотр данных получателя"""
    model = MailingListRecipient
    template_name = 'sending_messages/recipients_detail.html'
    context_object_name = 'recipient'


class MailingListRecipientCreateView(CreateView):
    """Добавление нового получателя"""
    model = MailingListRecipient
    form_class = RecipientsCreateForm
    template_name = 'sending_messages/recipient_form.html'
    success_url = reverse_lazy('sending_messages:recipients_list')


class MailingListRecipientUpdateView(UpdateView):
    """Редактирование данных получателя"""
    model = MailingListRecipient
    form_class = RecipientsCreateForm
    template_name = 'sending_messages/recipient_form.html'
    success_url = reverse_lazy('sending_messages:recipients_list')

    def get_success_url(self): # перенаправление на просмотр отредактированного получателя
        return reverse('sending_messages:recipient_detail', args=[self.kwargs.get('pk')])


class MailingListRecipientDeleteView(DeleteView):
    """Удаление получателя"""
    model = MailingListRecipient
    template_name = 'sending_messages/recipient_confirm_delete.html'
    success_url = reverse_lazy('sending_messages:recipients_list')


class LetterListView(ListView):
    """Список всех сообщений"""
    model = Letter
    template_name = 'sending_messages/letters_list.html'
    context_object_name = 'letters'


class LetterDetailView(DetailView):
    """Просмотр письма"""
    model = Letter
    template_name = 'sending_messages/letter_detail.html'
    context_object_name = 'letter'


class LetterCreateView(CreateView):
    """Создание нового письма"""
    model = Letter
    form_class = LetterCreateForm
    template_name = 'sending_messages/letter_form.html'
    success_url = reverse_lazy('sending_messages:letters_list')


class LetterUpdateView(UpdateView):
    """Редактирование письма"""
    model = Letter
    form_class = LetterCreateForm
    template_name = 'sending_messages/letter_form.html'
    success_url = reverse_lazy('sending_messages:letters_list')

    def get_success_url(self): # перенаправление на просмотр отредактированного письма
        return reverse('sending_messages:letter_detail', args=[self.kwargs.get('pk')])


class LetterDeleteView(DeleteView):
    """Удаление письма"""
    model = Letter
    template_name = 'sending_messages/letter_confirm_delete.html'
    success_url = reverse_lazy('sending_messages:letters_list')


class MailingListView(ListView):
    """Список всех рассылок"""
    model = Mailing
    template_name = 'sending_messages/mailing_list.html'
    context_object_name = 'mailings'


class MailingDetailView(DetailView):
    """Просмотр рассылки"""
    model = Mailing
    template_name = 'sending_messages/mailing_detail.html'
    context_object_name = 'mailing'


class MailingCreateView(CreateView):
    """Создание новой рассылки"""
    model = Mailing
    form_class = MailingCreateForm
    template_name = 'sending_messages/mailing_form.html'
    success_url = reverse_lazy('sending_messages:mailing_list')


class MailingUpdateView(UpdateView):
    """Редактирование рассылки"""
    model = Mailing
    form_class = MailingCreateForm
    template_name = 'sending_messages/mailing_form.html'
    success_url = reverse_lazy('sending_messages:mailing_list')

    def get_success_url(self): # перенаправление на просмотр отредактированной рассылки
        return reverse('sending_messages:mailing_detail', args=[self.kwargs.get('pk')])


class MailingDeleteView(DeleteView):
    """Удаление рассылки"""
    model = Mailing
    template_name = 'sending_messages/mailing_confirm_delete.html'
    success_url = reverse_lazy('sending_messages:mailing_list')


class AttemptToSendCreateView(CreateView):
    """Запуск попытки отправки рассылки"""
    model = AttemptToSend
    form_class = AttemptCreateForm
    template_name = 'sending_messages/attempt_form.html'
    success_url = reverse_lazy('sending_messages:attempts_list')

    def form_valid(self, form):
        # создаем объект попытки, но пока не сохраняем
        attempt = form.save(commit=False)
        mailing = attempt.mailing

        # Получаем содержимое письма
        message = mailing.letter.description if mailing.letter else ''
        subject = mailing.letter.title if mailing.letter else 'Без темы'

        # Получаем список email получателей
        recipients_emails = mailing.recipients.values_list('email', flat=True)

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
            attempt.mail_server_response = f'Успешно отправлено {result} писем'

        except Exception as e:
            # Фиксируем ошибку
            attempt.status = AttemptToSend.FAILED
            attempt.mail_server_response = f'Ошибка: {str(e)}'

        # Сохраняем попытку с обновленными данными
        attempt.save()
        return super().form_valid(form)


class AttemptToSendListView(ListView):
    """Список попыток отправки рассылок"""
    model = AttemptToSend
    template_name = 'sending_messages/attempts_list.html'
    context_object_name = 'attempts'


class AttemptToSendDetailView(DetailView):
    """Подробная информация о попытке отправки рассылки"""
    model = AttemptToSend
    template_name = 'sending_messages/attempt_detail.html'
    context_object_name = 'attempt'
