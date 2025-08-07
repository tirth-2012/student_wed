from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User

def to_title_case_with_space(text):
    cleaned = text.replace('_', ' ').replace('-', ' ')
    words = cleaned.split()
    result = ""
    for word in words:
        if word:
            result += word.capitalize() + " "
    return result.strip()

@receiver(pre_save, sender=User)
def format_username(sender, instance, **kwargs):
    if instance.username:
        instance.username = to_title_case_with_space(instance.username)