from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UsernameField, \
    UserCreationForm

from . import models


class LoginForm(AuthenticationForm):
    username = UsernameField(
        label='Username',
        min_length=4,
        max_length=32,
        widget=forms.TextInput(attrs={
            'autofocus': 'true', 'class': 'login__elem form__field mb-20',
            'placeholder': 'Input your username'
        }),
    )
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'login__elem form__field mb-20',
            'placeholder': 'Password here, please'
        }),
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'autofocus': 'true',
            'class': 'signup__elem form__field mb-20',
            'placeholder': 'Choose your username'
        }),
        min_length=4,
        max_length=32,
    )

    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'signup__elem form__field mb-20',
            'placeholder': 'Choose a strong password'
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={
            'class': 'signup__elem form__field mb-20',
            'placeholder': 'Confirm password'
        }),
        strip=False,
        help_text='Enter the same password as before, for verification.',
    )

    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'about', 'avatar', ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'signup__elem form__field mb-20',
                'placeholder': 'Your first name, ex. Vasya'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'signup__elem form__field mb-20',
                'placeholder': 'Your first name, ex. Pupkin'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'signup__elem form__field mb-20',
                'placeholder': 'Your E-mail'
            }),
            'about': forms.TextInput(attrs={
                'class': 'signup__elem form__field mb-20',
                'placeholder': 'Your bio'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'signup__elem form__field mb-20',
            }),
        }
    #
    # def clean(self):
    #     cleaned_data = super(SignUpForm, self).clean()
    #     password = cleaned_data.get("password")
    #     confirm_password = cleaned_data.get("confirm_password")
    #
    #     if password != confirm_password:
    #         raise forms.ValidationError(
    #             "Password and confirm password does not match."
    #         )
    #
    #     return self.cleaned_data
    #
    # def save(self, commit=True):
    #     user = super(SignUpForm, self).save(commit=False)
    #     user.set_password(self.cleaned_data["password"])
    #     if commit:
    #         user.save()
    #     return user
    pass
