# chatapp/models.py

import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class OneonOneRoom(models.Model):
    '''1対1 のチャットルーム'''

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    first_user = models.ForeignKey(
        get_user_model(),
        related_name='room_first_user',
        on_delete=models.CASCADE
    )
    second_user = models.ForeignKey(
        get_user_model(),
        related_name='room_second_user',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return f'{self.first_user.username} and {self.second_user.username}'


class GroupRoom(models.Model):
    '''人数制限なしのグループチャットルーム'''

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=20
    )
    owner = models.ForeignKey(
        get_user_model(),
        related_name='room_owner',
        on_delete=models.CASCADE
    )
    participant = models.ManyToManyField(
        get_user_model()
    )
    created_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return f


class Message(models.Model):
    '''チャットメッセージ'''

    room = models.ForeignKey(
        OneonOneRoom,
        related_name='message_room',
        on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        get_user_model(),
        related_name='message_sender',
        on_delete=models.CASCADE
    )
    content = models.CharField(
        max_length=100
    )
    timestamp = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'sender: {self.sender.username} ({self.content[:15]})'


class GroupMessage(models.Model):
    '''グループルームのチャットメッセージ'''
    room = models.ForeignKey(
        GroupRoom,
        related_name='message_room',
        on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        get_user_model(),
        related_name='group_message_sender',
        on_delete=models.CASCADE
    )
    content = models.CharField(
        max_length=100
    )
    timestamp = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'sender: {self.sender.username} ({self.content[:15]})'