from django.http import JsonResponse, Http404, HttpResponseBadRequest
from rest_framework.views import APIView

from smrpo.models.project import Project


class ProjectsView(APIView):
    """
        Return user's projects.
    """
    def get(self, request):
        user = request.user
        projects = Project.objects.filter(users=user)
        projects = [project.api_data for project in projects]

        return JsonResponse(projects, safe=False)


class ProjectView(APIView):
    """
        Return user's project by id.
    """
    @staticmethod
    def get_object(pk, user):
        try:
            return Project.objects.get(pk=pk, users=user)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = request.user
        project = self.get_object(pk, user)

        return JsonResponse(project.api_data, safe=False)
