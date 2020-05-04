from django.conf import settings
from django.db import models
from django.utils.timezone import now

from smrpo.models.story import Story

from django.core.exceptions import ValidationError


def higher_than_zero(value):
    if value <= 0:
        raise ValidationError(
            "Ocena časa za dokončanje naloge mora biti večja od 0.",
            params={'value': value},
        )


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True, blank=True)

    active = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    estimated_time = models.FloatField(validators=[higher_than_zero])

    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='assignee')
    assignee_awaiting = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='assignee_awaiting')
    assignee_accepted = models.DateTimeField(null=True, blank=True)

    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='tasks')

    finished_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name='finished_tasks')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_tasks')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['title', 'story']

    def __str__(self):
        return "{} - {} ({})".format(self.title, self.story.name, self.created_by)

    def finish(self, user):
        if self.assignee != user:
            return "Napaka pri zakljucevanju naloge. Uporabnik ni trenuten assignee!"

        self.finished = True
        self.finished_by = user
        self.save()

        return None

    def accept(self, user):
        if self.finished:
            return "Naloga je že zaključena"

        # Task has already been assigned to some user
        if self.assignee:
            return "Naloga je že dodeljena uporabniku, zato je ni možno sprejeti."

        # Task is waiting for assigned user's acception
        if self.assignee_awaiting and user != self.assignee_awaiting:
            return "Nalogo lahko sprejme le uporabnik, kateremu je bila dodeljena ({}).".format(self.assignee_awaiting.username)

        self.assignee_accepted = now()
        self.assignee_awaiting = None
        self.assignee = user
        self.save()

        return None

    def decline(self, user):
        if self.finished:
            return "Naloga je že zaključena."

        # Task is waiting for assigned user's acception
        if self.assignee_awaiting and self.assignee_awaiting != user:
            return "Nalogo lahko zavrne le uporabnik, kateremu je bila dodeljena ({}).".format(self.assignee_awaiting.username)

        if self.assignee and self.assignee == user:
            return "Nalogo lahko zavrne le uporabnik, kateremu je bila dodeljena ({}).".format(self.assignee_awaiting.username)

        self.assignee_awaiting = None
        self.assignee = None
        self.save()

        return None

    @property
    def api_data(self):
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            active=self.active,
            estimated_time=self.estimated_time,
            assignee=self.assignee.username if self.assignee else None,
            assignee_awaiting=self.assignee_awaiting.username if self.assignee_awaiting else None,
            created_by=self.created_by.username if self.created_by else None,
            finished_by=self.finished_by.username if self.finished_by else None,
            finished=self.finished,
            created=self.created,
            updated=self.updated
        )
