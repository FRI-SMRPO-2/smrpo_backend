# Generated by Django 3.0.4 on 2020-03-29 22:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smrpo', '0022_auto_20200329_2125'),
    ]

    operations = [
        migrations.RenameField(
            model_name='storypriority',
            old_name='text',
            new_name='name',
        ),
    ]
