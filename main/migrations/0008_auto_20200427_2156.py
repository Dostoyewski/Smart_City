# Generated by Django 3.0.3 on 2020-04-27 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20200427_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='status',
            field=models.IntegerField(choices=[(0, 'Сотрудник'), (1, 'Руководитель среднего звена'), (2, 'Руководитель высшего звена'), (3, 'Админ')], default=0),
        ),
    ]
