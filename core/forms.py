from django import forms
from django.core.exceptions import ObjectDoesNotExist

from . import models


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = models.Message
        fields = ['text', ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        message = super().save(commit=False)
        message.author = self.user
        if commit:
            message.save()
        return message
