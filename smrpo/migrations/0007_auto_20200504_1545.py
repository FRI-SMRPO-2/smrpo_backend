# Generated by Django 3.0.4 on 2020-05-04 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smrpo', '0006_auto_20200504_1433'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='task',
            unique_together={('title', 'story')},
        ),
    ]
