from django.contrib.auth import get_user_model
from .models import Purr
from hypothesis.extra.django import TestCase
from hypothesis.extra.django import from_model
from hypothesis import given


class PurrTest(TestCase):
    @given(from_model(Purr, user=from_model(get_user_model())))
    def test_create_purr(self, purr):
        self.assertTrue(len(purr.content) < 140)
        self.assertIsNone(purr.in_reply_to)


    @given(from_model(Purr, user=from_model(get_user_model()), in_reply_to=from_model(Purr, user=from_model(get_user_model()))))
    def test_create_reply_purr(self, purr):
        self.assertTrue(len(purr.content) < 140)
        self.assertIsNotNone(purr.in_reply_to)
        original = purr.in_reply_to
        self.assertTrue(purr in original.replies())
