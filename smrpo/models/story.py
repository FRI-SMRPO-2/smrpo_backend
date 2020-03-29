from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from smrpo.models.project import Project


class StoryPriority(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Story priorities"

    def __str__(self):
        return self.text

    @property
    def api_data(self):
        return dict(
            id=self.id,
            name=self.name
        )


class StoryTest(models.Model):
    text = models.CharField(max_length=255)
    story = models.ForeignKey('Story', on_delete=models.CASCADE, related_name='tests')

    def __str__(self):
        return self.text


class Story(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)
    business_value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='stories')
    priority = models.ForeignKey(StoryPriority, on_delete=models.PROTECT)

    created_by = models.ForeignKey('ProjectUser', on_delete=models.PROTECT, blank=True, related_name='created_stories')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['name', 'project']
        verbose_name_plural = "Stories"

    def __str__(self):
        return self.name

    @property
    def api_data(self):
        return dict(
            id=self.id,
            name=self.name,
            text=self.text,
            business_value=self.business_value,
            priority=self.priority.api_data,
            tests=list(self.tests.values('id', 'text')),
            project_id=self.project_id,
            created_by=self.created_by.api_data,
            created=self.created,
            updated=self.updated,
        )