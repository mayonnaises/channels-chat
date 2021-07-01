from django.contrib import admin

from .models import (
    GroupMessage,
    GroupRoom,
    OneonOneRoom,
    Message
)


admin.site.register(GroupMessage)
admin.site.register(GroupRoom)
admin.site.register(OneonOneRoom)
admin.site.register(Message)
