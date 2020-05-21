import datetime

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from smrpo.models.story import Story

from django.core.exceptions import ValidationError

from smrpo.models.work_session import WorkSession


def higher_than_zero(value):
    if value <= 0:
        raise ValidationError(
            "Ocena časa za dokončanje naloge mora biti večja od 0.",
            params={'value': value},
        )


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True, blank=True)

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

        # Get assignee work session and stop it
        active_work_session = self.active_work_session
        if active_work_session:
            active_work_session.stop_work()

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

        # Start work session on this task
        return self.start_work_session()

    def start_work_session(self):
        if self.finished:
            return "Naloga je že zaključena."

        if not self.assignee:
            return "Naloga mora imeti dodeljenega uporabnika, da se lahko prične z delom."

        if self.work_sessions.filter(active__isnull=True, user=self.assignee).exists():
            return "Dela na tej nalogi že poteka."

        work_session, created = WorkSession.objects.get_or_create(
            date=now(),
            user=self.assignee,
            task=self,
            defaults=dict(
                active=now()
            )
        )

        if not created:
            work_session.start_work()

        if not work_session:
            return 'Napaka pri začetku dela.'

        return None

    def create_work_sessions(self):
        # Create WorkSessions for every sprint day for every user
        start = self.story.sprint.start_date
        end = self.story.sprint.end_date

        while start <= end:
            start += datetime.timedelta(days=1)

            project = self.story.project
            for user in project.developers.all():
                WorkSession.objects.create(
                    date=start,
                    user=user,
                    task=self,
                )
                print(user)

            if not project.developers.filter(id=project.scrum_master_id).exists():
                WorkSession.objects.create(
                    date=start,
                    user=project.scrum_master,
                    task=self,
                )

            if not project.developers.filter(id=project.product_owner_id).exists() and project.product_owner != project.scrum_master:
                WorkSession.objects.create(
                    date=start,
                    user=project.product_owner,
                    task=self,
                )
            print(start)

    @property
    def active_work_session(self):
        return self.work_sessions.filter(active__isnull=False, user=self.assignee).last()

    def decline(self, user):
        if self.finished:
            return "Naloga je že zaključena."

        # Task is waiting for assigned user's acception
        if self.assignee_awaiting and self.assignee_awaiting != user:
            return "Nalogo lahko zavrne le uporabnik, kateremu je bila dodeljena ({}).".format(self.assignee_awaiting.username)

        if self.assignee and self.assignee != user:
            return "Nalogo lahko zavrne le uporabnik, kateremu je bila dodeljena ({}).".format(self.assignee.username)

        # Get assignee work session and stop it
        active_work_session = self.active_work_session
        if active_work_session:
            active_work_session.stop_work()

        self.assignee_awaiting = None
        self.assignee = None
        self.save()

        return None

    @property
    def api_data(self):
        active_work_session = self.active_work_session

        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            story_id=self.story_id,
            story_name=self.story.name,
            project_id=self.story.project_id,
            active=True if active_work_session else False,  # Task is active if there is any active work session
            active_work_session=active_work_session.api_data if active_work_session else None,
            estimated_time=self.estimated_time,
            assignee=self.assignee.username if self.assignee else None,
            assignee_awaiting=self.assignee_awaiting.username if self.assignee_awaiting else None,
            created_by=self.created_by.username if self.created_by else None,
            finished_by=self.finished_by.username if self.finished_by else None,
            finished=self.finished,
            created=self.created,
            updated=self.updated
        )


# TODO check when new users are added to perform the same for them
@receiver(post_save, sender=Task)
def task_post_save(sender, instance, created, **kwargs):
    if created:
        instance.create_work_sessions()
