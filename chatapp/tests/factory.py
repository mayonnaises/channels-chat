# chatapp/tests/factory.py
import datetime
import pytz

from factory import LazyAttribute, Sequence, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDateTime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from chatapp.models import OneonOneRoom

TZ_INFO = pytz.timezone(settings.TIME_ZONE)


class UserFactory(DjangoModelFactory):
    # create test user object
    class Meta:
        model = get_user_model()

    username = Sequence(lambda n: f'user-{n:05}')
    email = LazyAttribute(lambda n: f'{n.username}@test.com')
    is_staff = False
    is_active = True
    date_joined = FuzzyDateTime(
        start_dt=datetime.datetime(2021, 5, 1, tzinfo=TZ_INFO),
        end_dt=timezone.now()
    )


class ChatRoomFactory(DjangoModelFactory):
    # create test room object
    class Meta:
        model = OneonOneRoom

    first_user = SubFactory(UserFactory)
    second_user = SubFactory(UserFactory)
    created_at = FuzzyDateTime(
        start_dt=datetime.datetime(2021, 5, 1, tzinfo=TZ_INFO),
        end_dt=timezone.now()
    )