from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from smrpo.models.project import Project


class Sprint(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    expected_speed = models.FloatField()
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='sprints')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, related_name='created_sprints')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.start_date < timezone.now().date():
            raise ValidationError("Začetni datum ne sme biti v preteklosti")

        if not self.start_date <= self.end_date:
            raise ValidationError("Končni datum ne sme biti pred začetnim")

    @property
    def api_data(self):
        return dict(
            id=self.id,
            start_date=self.start_date,
            end_date=self.end_date,
            expected_speed=self.expected_speed,
            project=self.project,
            created=self.created,
            updated=self.updated,
        )
