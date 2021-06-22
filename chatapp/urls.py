# chatapp/urls.py

from django.urls import path

from .views import (
    GroupChatView,
    OneonOneChatView,
    RoomRedirectView,
    TopPageView
)


app_name = 'chatapp'

urlpatterns = [
    # page view
    path('', TopPageView.as_view(), name='top_page'),
    path('chat_room/<slug:room_pk>/', OneonOneChatView.as_view(), name='chat_room'),
    path('group/<slug:room_pk>/', GroupChatView.as_view(), name='group_room'),

    # redirect view
    path('room_redirect/<slug:user_pk>', RoomRedirectView.as_view(), name='room_redirect'),
]