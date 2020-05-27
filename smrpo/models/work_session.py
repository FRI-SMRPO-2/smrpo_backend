from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils.timezone import now


class WorkSession(models.Model):
    date = models.DateField()
    active = models.DateTimeField(null=True, blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task = models.ForeignKey('smrpo.Task', on_delete=models.CASCADE, related_name='work_sessions')

    total_seconds = models.IntegerField(default=0)
    estimated_seconds = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} ({}: {})".format(self.date, self.active or "/", self.user.username, self.task.title)

    class Meta:
        ordering = ('date', )

    def start_work(self):
        self.active = now()
        self.task.active = True
        self.task.save()

        self.save()
        return True

    def stop_work(self):
        n = now()
        seconds = (n - self.active).total_seconds()

        if (self.active + timedelta(seconds=seconds)).date() == self.date:
            self.total_seconds += seconds
        else:
            seconds_left = seconds
            ws = self
            while seconds_left > 0:
                if ws.active:
                    remaining_seconds = ((ws.active+timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0) - ws.active).total_seconds() - ws.total_seconds
                    ws.total_seconds += remaining_seconds
                    seconds_left -= remaining_seconds
                    ws.active = None
                    ws.save()
                    date = ws.date + timedelta(days=1)
                    ws = self.task.work_sessions.filter(date=date).first()
                    if not ws:
                        break
                    continue

                if ws.total_seconds + seconds_left >= 86400:
                    seconds_left -= ws.total_seconds
                    ws.total_seconds = 86400
                    ws.save()
                else:
                    ws.total_seconds += seconds_left
                    ws.save()
                    break

                date = ws.date + timedelta(days=1)
                ws = self.task.work_sessions.filter(date=date).first()
                if not ws:
                    break

        self.active = None
        self.task.active = False
        self.task.save()

        # TODO should change estimation based on this work session? subtract it?
        self.save()
        return True

    @property
    def api_data(self):
        return dict(
            id=self.id,
            date=self.date,
            active=self.active,
            total_seconds=self.total_seconds,
            estimated_seconds=self.estimated_seconds,
            user=self.user.username,
            user_id=self.user.id,
            task=self.task.title,
            task_id=self.task.id,
        )
