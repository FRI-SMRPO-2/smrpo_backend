# Generated by Django 3.0.4 on 2020-03-22 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smrpo', '0007_auto_20200322_2046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectuser',
            name='title',
        ),
    ]
