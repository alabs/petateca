from django.db import models
from serie.models import Serie

from django.contrib.auth.models import User
from django.core.validators import email_re
from django.contrib.auth.backends import ModelBackend

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    favorite_series = models.ManyToManyField(Serie, related_name="favorite_of")

def user_post_delete(sender, instance, **kwargs):
    try:
        UserProfile.objects.get(user=instance).delete()
    except:
        pass

def user_post_save(sender, instance, **kwargs):
    try:
        profile, new = UserProfile.objects.get_or_create(user=instance)
    except:
        pass

models.signals.post_delete.connect(user_post_delete, sender=User)
models.signals.post_save.connect(user_post_save, sender=User)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        if email_re.search(username):
            try:
                user = User.objects.get(email=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None
        return None

