# Generated by Django 3.0.3 on 2020-05-01 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telemetry', '0008_summary_approx'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Summary_Approx',
            new_name='SummaryApprox',
        ),
    ]