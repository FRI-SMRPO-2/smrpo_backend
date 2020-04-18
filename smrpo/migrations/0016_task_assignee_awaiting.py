# Generated by Django 3.0.4 on 2020-04-18 18:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smrpo', '0015_auto_20200418_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='assignee_awaiting',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignee_awaiting', to=settings.AUTH_USER_MODEL),
        ),
    ]