# Generated by Django 3.0.3 on 2020-05-01 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_userprofile_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='./static/images/avatars/default.png', null=True, upload_to='./static/images/avatars/', verbose_name='profile picture'),
        ),
    ]
