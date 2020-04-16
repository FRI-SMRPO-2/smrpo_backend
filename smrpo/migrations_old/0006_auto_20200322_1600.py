# Generated by Django 3.0.4 on 2020-03-22 16:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('smrpo', '0005_auto_20200321_1517'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProjectMember',
            new_name='ProjectUser',
        ),
        migrations.RenameModel(
            old_name='ProjectMemberRole',
            new_name='ProjectUserRole',
        ),
        migrations.RemoveField(
            model_name='project',
            name='members',
        ),
        migrations.AddField(
            model_name='project',
            name='users',
            field=models.ManyToManyField(related_name='projects', through='smrpo.ProjectUser', to=settings.AUTH_USER_MODEL),
        ),
    ]