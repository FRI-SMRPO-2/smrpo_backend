# Generated by Django 3.0.4 on 2020-05-04 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smrpo', '0003_auto_20200504_0904'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='unique_by_project_count_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
