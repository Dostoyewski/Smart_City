# Generated by Django 3.0.3 on 2020-04-30 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20200429_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='C:\\Users\\Федор\\Documents\\GIT\\Smart_City/static/images/avatars/default.png', null=True, upload_to='C:\\Users\\Федор\\Documents\\GIT\\Smart_City/static/images/avatars/', verbose_name='profile picture'),
        ),
    ]
