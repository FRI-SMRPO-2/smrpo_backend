from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView

from smrpo.models.project import Project
from smrpo.models.sprint import Sprint
from smrpo.models.story import Story

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


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

    """
        Add stories to the active sprint.
    """
    def put(self, request, sprint_id):
        user = request.user

        try:
            sprint = Sprint.objects.get(pk=sprint_id)
        except Sprint.DoesNotExist:
            return HttpResponse('Sprint ne obstaja.', status=404)

        if not user.is_superuser:
            if not sprint.project.scrum_master == user:
                return HttpResponse('Samo skrbnik metodologije lahko dodaja zgodbe v sprint.', status=403)

        active_sprint = sprint.project.active_sprint

        if not active_sprint:
            return HttpResponse("V projektu ni aktivnega sprinta.", status=400)
        logger.error("sprint")
        logger.error(sprint.api_data)
        logger.error("active sprint")
        logger.error(active_sprint.api_data)
        if sprint != active_sprint:
            return HttpResponse("Zgodbe lahko dodajaš le aktivnemu sprintu.", status=400)

        story_ids = request.data.get('story_ids', [])
        if not story_ids:
            return HttpResponse("Seznam zgodb je prazen.", status=400)

        stories = Story.objects.filter(pk__in=story_ids)

        story_errors = dict()
        new_speed = 0
        for story in stories:
            if story.realized:
                story_errors[story.id] = "Zgodba je že realizirana."
            elif not story.time_complexity:
                story_errors[story.id] = "Zgodba še nima določene časovne zahtevnosti."
            elif story.sprint:
                story_errors[story.id] = "Zgodba je že dodeljena sprintu."
            else:
                new_speed += story.time_complexity

        errors = []
        if new_speed + sprint.current_speed > sprint.expected_speed:
            errors.append(
                "Skupna časovna zahtevnost zgodb ({}) presega pričakovano hitrost sprinta ({}).".format(
                    new_speed + sprint.current_speed,
                    sprint.expected_speed
                )
            )

        if errors or story_errors:
            return JsonResponse(
                dict(
                    errors=errors,
                    story_errors=story_errors
                ), status=400
            )

        for story in stories:
            story.sprint = sprint
            try:
                story.save()
            except:
                return HttpResponse("Napaka pri dodajanje zgodb v sprint.", 400)

        return HttpResponse()
