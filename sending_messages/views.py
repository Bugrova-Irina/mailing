from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from sending_messages.models import MailingListRecipient, Letter, Mailing


class MainPageView(DetailView):
    """Класс для отображения главной страницы"""
    template_name = 'sending_messages/main.html'

    def get(self, request, *args, **kwargs):
        """Обработка get-запроса, рендеринг шаблона страницы"""
        return render(request, self.template_name)


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
    fields = ('email', 'recipient_name', 'comment')
    template_name = 'sending_messages/recipient_form.html'
    success_url = reverse_lazy('sending_messages:recipients_list')


class MailingListRecipientUpdateView(UpdateView):
    """Редактирование данных получателя"""
    model = MailingListRecipient
    fields = ('email', 'recipient_name', 'comment')
    template_name = 'sending_messages/recipient_form.html'
    success_url = reverse_lazy('sending_messages:recipients_list')

    def get_success_url(self): # перенаправление на просмотр отредактированного получателя
        return reverse('sending_messages:recipient_detail', args=[self.kwargs.get('pk')])


class MailingListRecipientDeleteView(DeleteView):
    """Удаление получателя"""
    model = MailingListRecipient
    template_name = 'sending_messages/recipient_confirm_delete.html'
    success_url = reverse_lazy('sending_messages:recipient_list')


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
    fields = ('title', 'description')
    template_name = 'sending_messages/letter_form.html'
    success_url = reverse_lazy('sending_messages:letters_list')


class LetterUpdateView(UpdateView):
    """Редактирование письма"""
    model = Letter
    fields = ('title', 'description')
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
    fields = ('start_sending', 'end_sending', 'status', 'letter', 'mailing_list_recipient')
    template_name = 'sending_messages/mailing_form.html'
    success_url = reverse_lazy('sending_messages:mailing_list')


class MailingUpdateView(UpdateView):
    """Редактирование рассылки"""
    model = Mailing
    fields = ('start_sending', 'end_sending', 'status', 'letter', 'mailing_list_recipient')
    template_name = 'sending_messages/mailing_list_form.html'
    success_url = reverse_lazy('sending_messages:mailing_list')

    def get_success_url(self): # перенаправление на просмотр отредактированной рассылки
        return reverse('sending_messages:mailing_detail', args=[self.kwargs.get('pk')])


class MailingDeleteView(DeleteView):
    """Удаление рассылки"""
    model = Mailing
    template_name = 'sending_messages/mailing_confirm_delete.html'
    success_url = reverse_lazy('sending_messages:mailing_list')
