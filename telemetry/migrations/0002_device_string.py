# Generated by Django 3.0.3 on 2020-04-28 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telemetry', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='string',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
