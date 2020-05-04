from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from smrpo.models.project import Project


class Sprint(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    expected_speed = models.FloatField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sprints')

    # Maybe change FK to ProjectUser if needed
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, related_name='created_sprints')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} ({} - {})".format(self.project, self.start_date, self.end_date)

    @property
    def is_active(self):
        now = timezone.now().date()
        if self.start_date <= now <= self.end_date:
            return True
        return False

    # TODO should be velocity, but we f*cked up, it iz what it iz now
    @property
    def current_speed(self):
        speed = self.stories.aggregate(sum=Sum('time_complexity'))['sum']
        return speed if speed else 0

    @property
    def api_data(self):
        return dict(
            id=self.id,
            start_date=self.start_date,
            end_date=self.end_date,
            expected_speed=self.expected_speed,
            project_id=self.project_id,
            created_by=self.created_by.username,
            created=self.created,
            updated=self.updated,
            stories=[x.api_data for x in self.stories.all()]
        )


@receiver(pre_save, sender=Sprint)
def sprint_pre_save(sender, instance, *args, **kwargs):
    start = instance.start_date
    end = instance.end_date

    if start < timezone.now().date():
        raise ValueError('Začetni datum ne sme biti v preteklosti.')

    if not start <= end:
        raise ValueError('Končni datum ne sme biti pred začetnim.')

    if instance.expected_speed <= 0.0:
        raise ValueError('Hitrost sprinta mora biti večja od 0.')

    # check if sprints overlap
    overlapping_sprints = Sprint.objects.filter(project=instance.project, start_date__lte=end, end_date__gte=start).exists()
    if overlapping_sprints:
            raise ValidationError('Datum sprinta se prekriva z že obstoječim.')
