from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.text import slugify
import pandas as pd
import datetime
import numpy as np
from django.conf import settings
# Create your models here.

GENDER = (
    (0, "MALE"),
    (1, "FEMALE")
)

STATUS = (
    (0, "Сотрудник"),
    (1, "Руководитель среднего звена"),
    (2, "Руководитель высшего звена"),
    (3, "Админ")
)


class UserProfile(models.Model):
    """
    Extended user model
    """
    # Ссылка на объект пользователя
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Имя
    name = models.CharField(max_length=50, blank=True)
    # Фамилия
    vorname = models.CharField(max_length=50, blank=True)
    # Отчество
    fathername = models.CharField(max_length=50, blank=True)
    gender = models.IntegerField(choices=GENDER, default=0)
    age = models.DateField(default=datetime.date(2000, 1, 1))
    # Должность
    position = models.CharField(max_length=50, blank=True)
    # Служебная переменная, определяющая уровень доступа
    status = models.IntegerField(choices=STATUS, default=0)
    # стаж
    exp = models.IntegerField(default=0)
    # Флаг, указывающий на заполненные дополнительные поля
    isFull = models.BooleanField(default=False)


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
        file = pd.read_excel(settings.BASE_DIR + settings.STATIC_ROOT + '/datafiles/staff_info.xlsx')
        if profile.user.email in file['Почта'].values:
            ind,  = np.where(file['Почта'].values == profile.user.email)
            ind = ind[0]
            names = file['ФИО'][ind].split()
            profile.name = names[0]
            profile.vorname = names[1]
            profile.fathername = names[2]
            profile.gender = 0 if file['Пол'][ind] else 1
            profile.age = datetime.date(datetime.date.today().year - int(file['Возраст'][ind]),
                                        datetime.date.today().month,
                                        datetime.date.today().day)
            profile.status = check_status(file['Должность'][ind])
            profile.position = file['Должность'][ind]
            profile.exp = file['Стаж'][ind]
            profile.user.is_staff = True
            profile.isFull = True
        profile.save()


post_save.connect(create_user_profile, sender=User)


def check_status(name):
    """
    This function helps to declare user status
    :param name: name of user's job
    :return: STATUS code
    """
    if 'администратор' in name.lower():
        return 3
    elif 'ведущий' in name.lower() or 'начальник' in name.lower():
        return 1
    elif 'директор' in name.lower():
        return 2
    else:
        return 0
