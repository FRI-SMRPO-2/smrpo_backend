from rest_framework import serializers

from smrpo.models.project import Project
from smrpo.serializers.project_user import ProjectUserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    users = ProjectUserSerializer(source='projectuser_set', many=True, read_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'description',
            'users',
            'deadline',
            'finished',
            'canceled',
            'created_by',
            'created'
        )
