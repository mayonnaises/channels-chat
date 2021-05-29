# chatapp/tests/test_consumers.py

from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .factory import ChatRoomFactory, UserFactory
from chatapp.models import OneonOneRoom


class ChatTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.room_factory = ChatRoomFactory
        cls.room_factory.create_batch(1)
        cls.room = OneonOneRoom.objects.latest('created_at')

        cls.user_factory = UserFactory
        cls.user_factory.create_batch(1)
        cls.user = get_user_model().objects.latest('date_joined')

        cls.url = reverse('chatapp:chat_room', kwargs={'room_pk': cls.room.pk})

    def test_auth_user_response(self):
        self.client.force_login(self.user)
        res = self.client.get(self.url)

        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('chatapp/one_on_one_chat.html')
        self.assertContains(res, self.room.pk)

    def test_anonymous_response(self):
        self.client.logout()
        res = self.client.get(self.url)

        # reject access
        self.assertEqual(res.status_code, HTTPStatus.FOUND)