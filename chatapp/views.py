# chatapp/views.py

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views.generic import TemplateView, View

from .models import OneonOneRoom, GroupRoom, Message


class TopPageView(TemplateView):
    template_name = 'chatapp/index.html'

    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'user_list': get_user_model().objects.all(),
        })
        return context


class OneonOneChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chatapp/one_on_one_chat.html'

    def get_chat_partner(self, room):
        if room.first_user != self.request.user:
            return room.first_user
        return room.second_user

    def get_context_data(self, room_pk):
        context = super().get_context_data()
        room = OneonOneRoom.objects.get(pk=room_pk)
        context.update({
            'room': room,
            'chat_partner': self.get_chat_partner(room),
            'message_list': Message.objects.filter(room=room).order_by('timestamp'),
        })
        return context


class RoomRedirectView(View):

    def get_chat_room(self, user_list):
        pk_sorted = sorted(user_list, key=lambda x: x.pk)

        try:
            return OneonOneRoom.objects.get(
                first_user=pk_sorted[0],
                second_user=pk_sorted[1])
        except OneonOneRoom.DoesNotExist:
            return OneonOneRoom.objects.create(
                first_user=pk_sorted[0],
                second_user=pk_sorted[1])

    def get(self, request, user_pk):
        req_user = self.request.user
        another_user = get_user_model().objects.get(pk=user_pk)


        if req_user != another_user and req_user.is_authenticated:
            room = self.get_chat_room([req_user, another_user])
            return redirect('chatapp:chat_room', room_pk=room.pk)
        return redirect('http://localhost:8000/admin/')


class GroupChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chatapp/group_chat.html'

    def get_context_data(self, room_pk):
        context = super().get_context_data()
        room = GroupRoom.objects.get(pk=room_pk)
        context.update({
            'room': room
        })
        return context