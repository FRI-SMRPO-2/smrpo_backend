from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from rest_framework.views import APIView


class RealizeStoriesView(APIView):
    """
        Mark stories as realized
    """
    def put(self, request, project_id):
        user = request.user

        return HttpResponse("OK", status=200)
