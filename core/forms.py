from django import forms
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from . import models


# class MessageCreateForm(forms.ModelForm):
#     input__attach = forms.FileField()
#
#     class Meta:
#         model = models.Message
#         fields = ['text', ]
#
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user')
#         attach = kwargs.pop('files')
#         super().__init__(*args, **kwargs)
#         self.user = user
#         self.attach = attach
#
#     def save(self, commit=True):
#         message = super().save(commit=False)
#         message.author = self.user
#         if commit:
#             message.save()
#             if self.attach:
#                 for _ in self.attach['file']:
#                     attach = models.Attachment.objects.create(file=_)
#                     attach.save()
#         return message


class MessageCreateForm(forms.Form):
    # We use forms.Form instead of forms.ModelForm, because we need to fill
    # 2 instances of 2 models: Message and Attachment
    attachments = forms.FileField()
    text = forms.CharField()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        attaches = kwargs.pop('files')
        super().__init__(*args, **kwargs)
        self.user = user
        self.attaches = attaches

    def is_valid(self):
        return (self.data['text'] or self.attaches) \
               and self.user.is_authenticated

    # method save like method save of ModelForm
    def save(self, commit=True):
        message = models.Message(text=self.data['text'])
        message.author = self.user
        attachments = []
        if commit:
            message.save()
            if self.attaches:
                for _ in self.attaches.getlist('attachments'):
                    attach = models.Attachment(
                        message=message, file=_, filename=_.name,
                        content_type=_.content_type)
                    attach.save()
                    attachments.append({
                        'url': attach.file.url,
                        'filename': attach.filename,
                        'content_type': attach.content_type
                    })
        return message, attachments
