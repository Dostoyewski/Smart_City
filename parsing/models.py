from django.db import models
from .vk_srapper import get_user_data, get_user_id
from Smart_City.settings import STATIC_ROOT

GENDER = (
    (0, "MALE"),
    (1, "FEMALE")
)
tok = '3a6c2d8a3a6c2d8a3a6c2d8a903a1da3d333a6c3a6c2d8a64c6cbd3fc1b20befe10ac47'


class AnketaManager(models.Manager):
    """
    Anketa creation manager, includes parsing
    """
    def create_anketa(self, name, vorname, fathername, gender, age, urlVK):
        anketa = self.create(name=name, vorname=vorname, fathername=fathername,
                             gender=gender, age=age, urlVK=urlVK)
        anketa.idVK = get_user_id(anketa.urlVK, tok)
        print('ok')
        anketa.save()
        get_user_data(anketa.urlVK, STATIC_ROOT)



class Anketa(models.Model):
    """
    Anket class for interview
    """
    name = models.CharField(max_length=50, blank=True)
    # Фамилия
    vorname = models.CharField(max_length=50, blank=True)
    # Отчество
    fathername = models.CharField(max_length=50, blank=True)
    gender = models.IntegerField(choices=GENDER, default=0)
    age = models.IntegerField(default=33)
    urlVK = models.CharField(default='123123', max_length=50)
    idVK = models.CharField(blank=True, max_length=10)
    objects = AnketaManager()
