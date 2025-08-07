from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

def normalize_username(text):
    text = text.replace('_', ' ').replace('-', ' ')
    words = text.split()
    result = ""
    for word in words:
        if word:
            result += word.capitalize() + " "
    return result.strip()

class CamelCaseUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is not None:
            username = normalize_username(username)
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
