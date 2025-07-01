# from django.forms import ModelForm
from django import forms

from sending_messages.models import Mailing, Letter
from users.forms import StyleFormMixin


class MailingCreateForm(StyleFormMixin, forms.ModelForm):
    """Класс формы для создания/редактирования рассылки"""
    class Meta:
        model = Mailing
        fields = ('start_sending', 'end_sending', 'status', 'letter', 'recipients')

    def __init__(self, *args, **kwargs):
        super(MailingCreateForm, self).__init__(*args, **kwargs)

        self.fields['start_sending'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Укажите дату старта рассылки'
        })
        self.fields['start_sending'].help_text = ''

        self.fields['end_sending'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ' Укажите дату окончания рассылки '
        })
        self.fields['end_sending'].help_text =''

        self.fields['status'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ' Укажите дату окончания рассылки '
        })
        self.fields['status'].help_text = ''

        self.fields['letter'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ' Укажите дату окончания рассылки '
        })
        self.fields['letter'].help_text = ''

        self.fields['recipients'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ' Укажите дату окончания рассылки '
        })
        self.fields['recipients'].help_text = ''


class LetterCreateForm(StyleFormMixin, forms.ModelForm):
    """Класс формы для создания/редактирования письма"""
    class Meta:
        model = Letter
        fields = ('title', 'description',)

    def __init__(self, *args, **kwargs):
        super(LetterCreateForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите тему письма'
        })
        self.fields['title'].help_text = ''

        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Добавьте содержимое письма'
        })
        self.fields['description'].help_text = ''
