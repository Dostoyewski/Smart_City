from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.text import slugify
# Create your models here.

GENDER = (
    (0, "MALE"),
    (1, "FEMALE")
)

STATUS = (
    (0, "Сотрудник"),
    (1, "Руководитель среднего звена"),
    (2, "Руководитель высшего звена"),
    (3, "Директор"),
    (3, "Админ")
)


class UserProfile(models.Model):
    """
    Extended user model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True)
    vorname = models.CharField(max_length=50, blank=True)
    fathername = models.CharField(max_length=50, blank=True)
    gender = models.IntegerField(choices=GENDER, default=0)
    age = models.IntegerField(default=18)
    position = models.CharField(max_length=50, blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
    exp = models.IntegerField(default=0)

    def __str__(self):
        return "%s's profile" % self.user


def create_user_profile(sender, instance, created, **kwargs):
    """
    This function will create UserProfile parallel with new User
    :param sender: NOT_USED
    :param instance: User object
    :param created: NOT_USED
    :param kwargs: User args
    :return:
    """
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)
        profile.user_url = slugify(profile.user.email+profile.user.first_name)
        profile.save()


post_save.connect(create_user_profile, sender=User)
