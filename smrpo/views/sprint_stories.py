from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView

from smrpo.models.project import Project
from smrpo.models.sprint import Sprint


class SprintStoriesView(APIView):
    """
        Get all sprint stories
    """
    def get(self, request, sprint_id):
        user = request.user

        try:
            sprint = Sprint.objects.get(id=sprint_id)
        except Sprint.DoesNotExist:
            return HttpResponse('Sprint s tem ID-jem ne obstaja', 404)

        try:
            project = Project.objects.get(sprints=sprint_id)
        except Project.DoesNotExist:
            return HttpResponse('Sprint ni del nobenega projekta', 400)

        # check if user is part of the project
        if not user.is_superuser:
            is_developer = project.developers.all().filter(pk=user.api_data()['id']).exists()
            if not (project.product_owner == user or project.scrum_master == user or is_developer):
                return HttpResponse('User is forbidden to access this resource.', status=403)

        return JsonResponse(sprint.api_data, safe=False)
