from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import BooleanField, ModelForm, forms

from users.models import User


class StyleFormMixin:
    """
    Класс-миксин для стилизации полей формы
    создания/редактирования пользователя
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма регистрации пользователя"""

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # удаляем стандартное поле username, чтобы не было конфликта между
        # кастомной моделью пользователя и стандартной формой регистрации Django
        self.fields.pop("username", None)

    def clean_email(self):
        """Проверяем email нового пользователя на уникальность"""
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


class UserForm(StyleFormMixin, ModelForm):
    """Форма редактирования пользователя"""

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "phone",
            "country",
            "avatar",
        )


class ManagerForm(StyleFormMixin, ModelForm):
    """Форма редактирования пользователя менеджером"""

    class Meta:
        model = User
        fields = (
            "is_active",
        )
