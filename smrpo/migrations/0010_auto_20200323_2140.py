# Generated by Django 3.0.4 on 2020-03-23 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smrpo', '0009_auto_20200323_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=60, unique=True),
        ),
    ]
