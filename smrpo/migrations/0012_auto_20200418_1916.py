# Generated by Django 3.0.4 on 2020-04-18 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smrpo', '0011_remove_task_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='canceled_by',
        ),
        migrations.RemoveField(
            model_name='task',
            name='status',
        ),
    ]
