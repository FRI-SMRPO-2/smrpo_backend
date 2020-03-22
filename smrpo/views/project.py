from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from smrpo.models.project import Project
from smrpo.serializers.project import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
        """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(created_by=self.request.user)
