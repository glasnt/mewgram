from django.contrib.auth import get_user_model
from hypothesis.extra.django import TestCase
from hypothesis.extra.django import from_model
from hypothesis import given


class UsersManagersTests(TestCase):

    @given(from_model(get_user_model()))
    def test_create_user(self, user):
#        User = get_user_model()
#        user = User.objects.create_user(email='normal@user.com', display_name='user', password='foo')
#        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            get_user_model().objects.create_user()
        with self.assertRaises(TypeError):
            get_user_model().objects.create_user(email='')
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='', password="foo")
"""
    @given(from_model(CustomUser, is_active=True, is_staff=True, is_superuser=True))
    def test_create_superuser(self, admin_user):
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)
"""
