from rest_framework import serializers

from smrpo.models.project import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'description',
            'deadline',
            'finished',
            'canceled',
            'created_by',
            'created'
        )
