from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.dateparse import parse_date

from smrpo.models.project import Project
from smrpo.models.task import Task


class Sprint(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    expected_speed = models.FloatField()
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='sprints')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, related_name='created_sprints')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def api_data(self):
        return dict(
            id=self.id,
            start_date=self.start_date,
            end_date=self.end_date,
            expected_speed=self.expected_speed,
            project_id=self.project_id,
            created=self.created,
            updated=self.updated,
        )


@receiver(pre_save, sender=Sprint)
def task_pre_save(sender, instance, *args, **kwargs):
    start = instance.start_date
    end = instance.end_date
    speed = instance.expected_speed

    if start < timezone.now().date():
        raise ValueError("Začetni datum ne sme biti v preteklosti")

    if not start <= end:
        raise ValueError("Končni datum ne sme biti pred začetnim")

    if speed < 0.0:
        raise ValueError("Hitrost sprinta mora biti večja od 0")
