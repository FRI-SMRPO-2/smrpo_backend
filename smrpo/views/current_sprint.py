from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from rest_framework.views import APIView

from smrpo.models.sprint import Sprint


class ActiveSprintView(APIView):
    """
        Get active sprint for given project
    """
    def get(self, request, project_id):
        user = request.user

        try:
            # get current sprint
            now = timezone.now()

            sprints = Sprint.objects.filter(project_id=project_id)

            if not user.is_superuser:
                sprints.filter(
                    Q(project__scrum_master=user) | Q(project__product_owner=user) | Q(project__developers=user)
                ).distinct()

            sprint = sprints.get(start_date__lte=now, end_date__gte=now)
            return JsonResponse(sprint.api_data, safe=False)
        except Sprint.DoesNotExist:
            return HttpResponse('Trenutno ni aktiven noben sprint!', status=404)
