# Generated by Django 3.0.4 on 2020-03-23 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smrpo', '0011_remove_projectuserrole_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectuserrole',
            old_name='description',
            new_name='title',
        ),
    ]