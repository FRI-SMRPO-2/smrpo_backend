# Generated by Django 3.0.4 on 2020-04-18 16:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smrpo', '0006_auto_20200418_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='developers',
            field=models.ManyToManyField(related_name='developers', to=settings.AUTH_USER_MODEL),
        ),
    ]
