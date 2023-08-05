try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
    get_user_model = lambda: User


def get_username_field():
    return get_user_model().USERNAME_FIELD
