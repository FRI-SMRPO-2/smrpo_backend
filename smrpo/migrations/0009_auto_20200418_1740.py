# Generated by Django 3.0.4 on 2020-04-18 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smrpo', '0008_auto_20200418_1715'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='title',
            new_name='name',
        ),
    ]