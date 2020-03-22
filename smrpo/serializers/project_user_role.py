from rest_framework import serializers

from smrpo.models.project_user import ProjectUserRole


class ProjectUserRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectUserRole
        fields = ('id', 'title', 'description')
