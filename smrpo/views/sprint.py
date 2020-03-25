from django.http import JsonResponse
from rest_framework.views import APIView

from smrpo.models.sprint import Sprint


class SprintsView(APIView):
    """
        Get all sprints
    """
    def get(self, request):
        # query parameter
        project = request.GET.get('project')

        # get all sprints
        sprints = Sprint.objects.all()

        if project:
            sprints = sprints.filter(project_id=project)

        sprints = [sprint.api_data for sprint in sprints]

        return JsonResponse(sprints, safe=False)

    """
        Return project roles
    """
    def post(self, request):
        pass
        #project_roles = ProjectUserRole.objects.all()
        #project_roles = [project_role.api_data for project_role in project_roles]
        #return JsonResponse(project_roles, safe=False)
