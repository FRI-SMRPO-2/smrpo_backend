# Generated by Django 3.0.4 on 2020-04-18 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smrpo', '0008_auto_20200418_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='closed',
        ),
    ]
