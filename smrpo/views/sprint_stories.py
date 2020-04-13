from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView

from smrpo.models.project import Project
from smrpo.models.project_user import ProjectUser
from smrpo.models.sprint import Sprint


class SprintStoriesView(APIView):
    """
        Get all sprint stories
    """
    def get(self, request, sprint_id):
        user = request.user

        sprint = Sprint.objects.get(id=sprint_id)
        if not sprint:
            return HttpResponse('Sprint s tem ID-jem ne obstaja', 404)

        project = Project.objects.get(sprints=sprint_id)

        if not project:
            return HttpResponse('Sprint ni del nobenega projekta', 400)

        # check if user is part of the project
        if not user.is_superuser:
            try:
                # Check if user is part of the project
                ProjectUser.objects.filter(
                    Q(project_id=project.id),
                    Q(project__scrum_master__user=user) | Q(project__product_owner__user=user) | Q(
                        project__developers__user=user)
                )
            except ProjectUser.DoesNotExist:
                return HttpResponse('User is forbidden to access this resource.', status=403)

        return JsonResponse(sprint.api_data, safe=False)
