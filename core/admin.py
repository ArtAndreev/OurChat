from django.contrib import admin

from . import models

# Register your models here.


class ChatRoomAdmin(admin.ModelAdmin):
    search_fields = ['name']


class ChatDialogAdmin(admin.ModelAdmin):
    pass


class MessageAdmin(admin.ModelAdmin):
    list_display = ['author', 'text']
    search_fields = ['author', 'text']


# admin.site.register(models.ChatRoom, ChatRoomAdmin)
# admin.site.register(models.ChatDialog, ChatDialogAdmin)
#
# admin.site.register(models.RoomMessage, MessageAdmin)
# admin.site.register(models.DialogMessage, MessageAdmin)
