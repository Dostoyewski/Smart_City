# Generated by Django 3.0.3 on 2020-04-29 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20200429_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='static/images/avatars/default.png', null=True, upload_to='static/images/avatars/', verbose_name='profile picture'),
        ),
    ]
