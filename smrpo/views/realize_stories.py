from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from rest_framework.views import APIView

from smrpo.models.project import Project
from smrpo.models.story import Story


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
                return HttpResponse("Projekt ne obstaja ali pa uporabnik ni produktni vodja", status=404)

        # get story IDs from request
        story_ids = request.data.get('stories')

        if not story_ids or not isinstance(story_ids, list):
            return HttpResponse("ID-ji uporabniških zgodb niso podani ali pa niso podani kot seznam", status=400)

        stories = []
        for story_id in story_ids:
            try:
                # get story from the database
                now = timezone.now()
                story = Story.objects.filter(project=project, sprint__start_date__lte=now,
                                             sprint__end_date__gte=now).distinct().get(pk=story_id)

                # check if story is already realized
                if story.realized:
                    return HttpResponse("Zgodba {0} je že realizirana".format(str(story_id)), status=400)

                # check if story is finished
                if not story.are_all_tasks_finished():
                    return HttpResponse("Zgodba {0} še nima zaključenih vseh nalog".format(str(story_id)), status=400)

                # all checks passed, add to list
                stories.append(story)
            except Story.DoesNotExist:
                return HttpResponse("Uporabniša zgodba {0} ne obstaja ali pa ni del trenutnega sprinta".format(str(story_id)), status=404)

        # update status of all the stories
        for story in stories:
            story.realized = True
            story.save()

        return JsonResponse([x.api_data for x in stories], safe=False, status=200)
