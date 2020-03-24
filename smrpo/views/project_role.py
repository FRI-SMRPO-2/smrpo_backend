from django.http import JsonResponse
from rest_framework.views import APIView

from smrpo.models.project_user import ProjectUserRole


class ProjectRolesView(APIView):
    """
        Return project roles
    """
    def get(self, request):
        project_roles = ProjectUserRole.objects.all()
        project_roles = [project_role.api_data for project_role in project_roles]
        return JsonResponse(project_roles, safe=False)
