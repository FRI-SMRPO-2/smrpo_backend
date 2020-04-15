from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from rest_framework.views import APIView

from smrpo.models.sprint import Sprint


class ActiveSprintView(APIView):
    """
        Get all sprint stories
    """
    def get(self, request, project_id):
        try:
            # get current sprint
            now = timezone.now()
            sprint = Sprint.objects.filter(project_id=project_id).get(start_date__lte=now, end_date__gte=now)
            return JsonResponse(sprint.api_data, safe=False)
        except Sprint.DoesNotExist:
            return HttpResponse('Trenutno ni aktiven noben sprint!', 404)
