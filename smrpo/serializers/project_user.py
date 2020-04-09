from rest_framework import serializers

from smrpo.models.project_user import ProjectUser


class ProjectUserSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='user.get_full_name')
    username = serializers.ReadOnlyField(source='user.email')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = ProjectUser
        fields = ('id', 'name', 'username', 'email')
