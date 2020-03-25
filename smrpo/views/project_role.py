from django.http import JsonResponse
from rest_framework.views import APIView

from smrpo.models.project_user import ProjectUserRole


class ProjectRolesView(APIView):
    """
        Return project roles
    """
    def get(self, request):
        project_roles = list(ProjectUserRole.objects.all().values())
        return JsonResponse(project_roles, safe=False)
