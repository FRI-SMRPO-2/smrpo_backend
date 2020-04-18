from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from rest_framework.views import APIView

from smrpo.models.project import Project


class RealizeStoriesView(APIView):
    """
        Mark stories as realized
    """
    def put(self, request, project_id):
        user = request.user

        if user.is_superuser:
            project = Project.objects.get(pk=project_id)
        else:
            try:
                project = Project.objects.filter(product_owner=user).distinct().get(pk=project_id)
            except Project.DoesNotExist:
                return HttpResponse("Projekt ne obstaja ali pa uporabnik ni product owner", status=404)

        # TODO: mark stories as realized

        return JsonResponse(project.api_data, status=200)
