# Generated by Django 3.0.4 on 2020-04-16 18:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smrpo', '0003_auto_20200416_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='developers',
            field=models.ManyToManyField(blank=True, null=True, related_name='developers', to=settings.AUTH_USER_MODEL),
        ),
    ]
