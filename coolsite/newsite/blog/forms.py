from django import forms
from blog.models import *
from blog.utils import CustomCaptchaTextInput
from django.contrib.auth.forms import UserCreationForm, User, AuthenticationForm
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cat"].empty_label = "Категория не выбрана"

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) > 200:
            raise ValidationError("Заголовок должен быть не больше 200 символов")
        return title

    class Meta:
        model = Blog
        fields = ["title", "cat", "content", "photo", "is_published"]

        widgets ={
            "title": forms.TextInput(attrs={'class': 'form-input', "placeholder": "Название рецепта"}),
            "content": forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input-name', "placeholder": "не менее 5 символов"}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-input-email', "placeholder": "example@example.ru"}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-input-password'}))
    password2 = forms.CharField(label='Повтор пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-input-password'}))
    captcha = CaptchaField(label="Каптча",
                           widget=CustomCaptchaTextInput(attrs={'class': 'form-input', "placeholder": "введите текст с картинки"}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input-name'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input-password'}))
    captcha = CaptchaField(label="Каптча",
                           widget=CustomCaptchaTextInput(attrs={'class': 'form-input', "placeholder": "введите текст с картинки"}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255,
                           widget=forms.TextInput(attrs={'class': 'form-input-name', "placeholder": "введите имя"}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-input-email', "placeholder": "example@example.ru"}))
    content = forms.CharField(label="Текст", widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField(label="Каптча",
                           widget=CustomCaptchaTextInput(attrs={'class': 'form-input', "placeholder": "введите текст с картинки"}))

