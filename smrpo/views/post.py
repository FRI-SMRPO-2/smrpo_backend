from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView


class PostView(APIView):
    """
        Add post to project
    """
    def post(self, request, project_id):
        return JsonResponse("OK", safe=False, status=200)
