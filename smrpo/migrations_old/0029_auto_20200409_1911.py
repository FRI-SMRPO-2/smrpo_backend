# Generated by Django 3.0.4 on 2020-04-09 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smrpo', '0028_auto_20200409_2026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='project_owner',
        ),
        migrations.RemoveField(
            model_name='projectuser',
            name='role',
        ),
        migrations.AddField(
            model_name='project',
            name='product_owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='product_owner', to='smrpo.ProjectUser'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ProjectUserRole',
        ),
    ]