from django.contrib import admin

from . import models

# Register your models here.


class MessageAdmin(admin.ModelAdmin):
    list_display = ['author', 'text']
    search_fields = ['author', 'text']


admin.site.register(models.Message, MessageAdmin)
