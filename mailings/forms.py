from django import forms

from mailings.models import AttemptToSend, Letter, Mailing, Recipients
from users.forms import StyleFormMixin


class MailingCreateForm(StyleFormMixin, forms.ModelForm):
    """Класс формы для создания/редактирования рассылки"""

    class Meta:
        model = Mailing
        fields = ("start_sending", "end_sending", "status", "letter", "recipients")

    def __init__(self, *args, **kwargs):
        super(MailingCreateForm, self).__init__(*args, **kwargs)

        self.fields["start_sending"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Укажите дату старта в формате гггг-мм-дд чч:мм",
            }
        )
        self.fields["start_sending"].help_text = ""

        self.fields["end_sending"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": " Укажите дату окончания в формате гггг-мм-дд чч:мм",
            }
        )
        self.fields["end_sending"].help_text = ""

        self.fields["status"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": " Укажите дату окончания рассылки ",
            }
        )
        self.fields["status"].help_text = ""

        self.fields["letter"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": " Укажите дату окончания рассылки ",
            }
        )
        self.fields["letter"].help_text = ""

        self.fields["recipients"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": " Укажите дату окончания рассылки ",
            }
        )
        self.fields["recipients"].help_text = ""


class MailingManagerUpdateForm(StyleFormMixin, forms.ModelForm):
    """
    Класс для редактирования рассылки
    с возможностью перевода в статус 'Завершена'
    """
    class Meta:
        model = Mailing
        fields = ("status",)
        labels = {
            "status": "Статус рассылки"
        }
        help_texts = {
            "status": "Только для изменения статуса менеджером"
        }


class LetterCreateForm(StyleFormMixin, forms.ModelForm):
    """Класс формы для создания/редактирования письма"""

    class Meta:
        model = Letter
        fields = (
            "title",
            "description",
        )

    def __init__(self, *args, **kwargs):
        super(LetterCreateForm, self).__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите тему письма"}
        )
        self.fields["title"].help_text = ""

        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Добавьте содержимое письма"}
        )
        self.fields["description"].help_text = ""


class RecipientsCreateForm(StyleFormMixin, forms.ModelForm):
    """Класс формы создания/редактирования получателя рассылки"""

    class Meta:
        model = Recipients
        fields = ("email", "recipient_name", "comment")

    def __init__(self, *args, **kwargs):
        super(RecipientsCreateForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите адрес электронной почты"}
        )
        self.fields["email"].help_text = ""

        self.fields["recipient_name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите фамилию, имя, отчество клиента",
            }
        )
        self.fields["recipient_name"].help_text = ""

        self.fields["comment"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Оставьте свой комментарий"}
        )
        self.fields["comment"].help_text = ""


class AttemptCreateForm(StyleFormMixin, forms.ModelForm):
    """Класс для создания попытки отправки рассылки"""

    class Meta:
        model = AttemptToSend
        fields = ("mailing",)

    def __init__(self, *args, **kwargs):
        super(AttemptCreateForm, self).__init__(*args, **kwargs)

        self.fields["mailing"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Выберите рассылку"}
        )
        self.fields["mailing"].help_text = ""
