from rest_framework import serializers

from smrpo.models.task import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'users',
            'status',
            'finished_by',
            'canceled_by',
            'created_by',
            'finished',
            'canceled',
            'created'
        )
