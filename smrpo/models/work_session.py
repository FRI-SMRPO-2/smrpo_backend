from django.conf import settings
from django.db import models
from django.utils.timezone import now


class WorkSession(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task = models.ForeignKey('smrpo.Task', on_delete=models.CASCADE, related_name='work_sessions')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} ({}: {})".format(self.start, self.end or "/", self.user.username, self.task.title)

    class Meta:
        ordering = ('start', )

    def stop_work(self):
        self.end = now()
        self.save()
        return True

    @property
    def api_data(self):
        return dict(
            id=self.id,
            start=self.start,
            end=self.end,
            user=self.user.username,
            user_id=self.user.id,
            task=self.task.title,
            task_id=self.task.id,
        )
