# Generated by Django 3.0.4 on 2020-05-18 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smrpo', '0007_auto_20200504_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='sprint',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stories', to='smrpo.Sprint'),
        ),
    ]
