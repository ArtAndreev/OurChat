from django.db import models

from authentication.models import User

# Create your models here.


class Message(models.Model):
    author = models.ForeignKey(User, verbose_name='Author',
                               on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Message text', null=False)
    date = models.DateTimeField(verbose_name='Date', auto_now_add=True)

    class Meta:
        verbose_name = 'Chat message'
        verbose_name_plural = 'Chat messages'

    def __str__(self):
        return 'At {0} by {1}'.format(self.date, self.author)


class ChatRoom(models.Model):
    pass
