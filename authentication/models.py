from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    email = models.EmailField(verbose_name='email', blank=False, unique=True)
    avatar = models.ImageField(blank=True, verbose_name='User avatar')
    about = models.TextField(blank=True, max_length=100, verbose_name='About')

    class Meta:
        verbose_name = 'Chat user'
        verbose_name_plural = 'Chat users'

    def __str__(self):
        return self.username
