from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    # overriding base attributes of AbstractUser
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        'username',
        max_length=32,
        unique=True,
        help_text=
            'Required. 32 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    email = models.EmailField('email', blank=False, unique=True)

    # customizing
    avatar = models.ImageField(blank=True, verbose_name='User avatar')
    about = models.TextField(blank=True, max_length=100, verbose_name='About')

    class Meta:
        verbose_name = 'Chat user'
        verbose_name_plural = 'Chat users'

    def __str__(self):
        return self.username
