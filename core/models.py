from django.db import models

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
    text = models.TextField(verbose_name='Message text', null=False)
    date = models.DateTimeField(verbose_name='Date', auto_now_add=True)

    class Meta:
        # abstract = True
        verbose_name = 'Chat message'
        verbose_name_plural = 'Chat messages'

    def __str__(self):
        return 'At {0} by {1}'.format(self.date, self.author)


# class RoomMessage(Message):
#     room = models.ForeignKey(ChatRoom, verbose_name='From dialog',
#                              on_delete=models.CASCADE)
#
#
# class DialogMessage(Message):
#     dialog = models.ForeignKey(ChatDialog, verbose_name='From room',
#                                on_delete=models.CASCADE)
