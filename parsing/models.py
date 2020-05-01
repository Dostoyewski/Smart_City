from django.db import models


GENDER = (
    (0, "MALE"),
    (1, "FEMALE")
)


class AnketaManager(models.Manager):
    """
    Anketa creation manager, includes parsing
    """
    def create_anketa(self, name, vorname, fathername, gender, age, urlVK):
        anketa = self.create(name=name, vorname=vorname, fathername=fathername,
                             gender=gender, age=age, urlVK=urlVK)


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
    objects = AnketaManager()
