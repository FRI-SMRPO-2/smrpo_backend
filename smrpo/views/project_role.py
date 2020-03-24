from django.http import JsonResponse
from rest_framework.views import APIView


class ProjectRolesView(APIView):
    """
        Return project roles
    """
    def get(self, request):
        return JsonResponse("works", safe=False)
