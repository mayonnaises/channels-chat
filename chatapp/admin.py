from django.contrib import admin

from .models import GroupRoom, OneonOneRoom, Message


admin.site.register(GroupRoom)
admin.site.register(OneonOneRoom)
admin.site.register(Message)