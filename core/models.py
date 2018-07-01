from os import path
from hashlib import sha256

from django.db import models
from chat.settings import SECRET_KEY

from authentication.models import User

# Create your models here.


# class ChatDialogManager(models.Manager):
#     def get_user_dialogs(self, user_id):
#         user_dialogs = self.filter(user1=user_id)
#         user_dialogs += self.filter(user2=user_id)
#
#         return user_dialogs.order_by('-id')
#
#
# class ChatRoomManager(models.Manager):
#     def get_user_rooms(self, user_id):
#         return self.filter(users=user_id).order_by('-id')
#
#
# class ChatDialog(models.Model):
#     user1 = models.ForeignKey(User, verbose_name='First person',
#                               related_name='user1',
#                               on_delete=models.CASCADE)
#     user2 = models.ForeignKey(User, verbose_name='Second person',
#                               related_name='user2',
#                               on_delete=models.CASCADE)
#
#     objects = ChatDialogManager()
#
#
# class ChatRoom(models.Model):
#     name = models.CharField(max_length=32, null=False)
#     avatar = models.ImageField(verbose_name='Chat avatar', blank=True)
#     users = models.ManyToManyField(User, verbose_name='Persons')
#
#     objects = ChatRoomManager()
#
#
# class MessageManager(models.Manager):
#     def get_all_messages(self):
#         return self.order_by('-id')
#
#     def get_messages_for_polling(self):
#         return self.order_by('-id')[:20]


class Message(models.Model):
    author = models.ForeignKey(User, verbose_name='Author',
                               on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Message text', null=True)
    date = models.DateTimeField(verbose_name='Date', auto_now_add=True)

    class Meta:
        # abstract = True
        verbose_name = 'Chat message'
        verbose_name_plural = 'Chat messages'

    def __str__(self):
        return 'At {0} by {1}'.format(self.date, self.author)


def upload_file_directory(instance, filename):
    # file will be uploaded to MEDIA_ROOT/chat/attachments/user_<id>/<filename>
    return 'chat/attachments/user_{0}/{1}{2}'.format(
        instance.message.author.id,
        sha256((filename + str(instance.message.date)).encode('utf-8')).hexdigest(),
        path.splitext(filename)[1]  # file extension
    )


class Attachment(models.Model):
    message = models.ForeignKey(Message, verbose_name='From',
                                on_delete=models.CASCADE)
    file = models.FileField(verbose_name='Attach file',
                            upload_to=upload_file_directory)
    filename = models.TextField(verbose_name='Filename', blank=True)
    content_type = models.TextField(verbose_name='Content-type', blank=True)


# class RoomMessage(Message):
#     room = models.ForeignKey(ChatRoom, verbose_name='From dialog',
#                              on_delete=models.CASCADE)
#
#
# class DialogMessage(Message):
#     dialog = models.ForeignKey(ChatDialog, verbose_name='From room',
#                                on_delete=models.CASCADE)
