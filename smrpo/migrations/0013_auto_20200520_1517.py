# Generated by Django 3.0.4 on 2020-05-20 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smrpo', '0012_auto_20200520_1508'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='worksession',
            unique_together=set(),
        ),
    ]