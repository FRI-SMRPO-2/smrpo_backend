from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.views import APIView

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


class ProjectView(APIView):
    """
        Return user's projects.
    """
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        user = request.user
        projects = Project.objects.filter(users=user)
        projects = [project.api_data for project in projects]
        return JsonResponse(projects, safe=False)
