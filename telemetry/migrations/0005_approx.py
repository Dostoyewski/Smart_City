# Generated by Django 3.0.3 on 2020-04-30 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telemetry', '0004_auto_20200428_1743'),
    ]

    operations = [
        migrations.CreateModel(
            name='Approx',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('array', models.CharField(default='[]', max_length=100)),
                ('piers', models.FloatField(default=1)),
            ],
        ),
    ]
