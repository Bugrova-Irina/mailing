from django.forms import ModelForm

from sending_messages.models import Mailing
from users.forms import StyleFormMixin


class MailingCreateForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        fields = ('start_sending', 'end_sending', 'status', 'letter', 'recipients')
