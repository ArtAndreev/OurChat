from asgiref.sync import async_to_sync
from django import forms
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from . import models
from channels.layers import get_channel_layer


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

        # consumers.ChatConsumer.send(text_data=(message, attachments))
        channel_layer = get_channel_layer()
        # , text_data={
        #     'message': message,
        #     'attachments': attachments
        # })
        async_to_sync(channel_layer.send)(message={'message': message})
        # async_to_sync(channel_layer.send_message)(text_data={
        #     'message': message,
        #     'attachments': attachments
        # })
        return message, attachments
