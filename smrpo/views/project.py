from django.http import JsonResponse, Http404, HttpResponseBadRequest
from rest_framework.views import APIView

from smrpo.models.project import Project


class ProjectsView(APIView):
    """
        Return user's projects.
    """
    def get(self, request):
        role = request.GET.get('role')
        user = request.user

        # Get user's projects
        projects = Project.objects.filter(users=user)

        # If role parameter was passed return projects that match provided user role.
        if role:
            projects = projects.filter(projectuser__role__title=role)

        projects = [project.api_data for project in projects]

        return JsonResponse(projects, safe=False)

    def post(self, request):
        data = request.data

        # check if all fields are set
        name = data['name']

        if data['users'] and len(data['users']):
            pass

        return JsonResponse("test", safe=False)


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
