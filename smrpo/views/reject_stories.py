from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from rest_framework.views import APIView

from smrpo.models.project import Project
from smrpo.models.story import Story


class RejectStoriesView(APIView):
    """
        Reject stories and return them to backlog
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
            return HttpResponse("Uporabniškihe zgodbe niso podane ali pa niso podane kot seznam", status=400)

        stories = []
        for item in story_ids:
            story_id = item['id']
            comment = item['comment']
            try:
                # get story from the database
                now = timezone.now()
                story = Story.objects.filter(project=project, sprint__start_date__lte=now,
                                             sprint__end_date__gte=now).distinct().get(pk=story_id)

                # check if story is already rejected
                # if story.rejection_comment is not None or story.rejection_comment != "":
                # if story.rejection_comment:
                #    return HttpResponse("Zgodba {0} je že zavrnjena".format(str(story_id)), status=400)

                # check if story is already realized
                if story.realized:
                    return HttpResponse("Zgodba {0} je že realizirana".format(str(story_id)), status=400)

                # all checks passed, add to list with comment
                stories.append((story, comment))
            except Story.DoesNotExist:
                return HttpResponse("Uporabniška zgodba {0} ne obstaja ali pa ni del trenutnega sprinta".format(str(story_id)), status=404)

        # update status of all the stories
        for (story, comment) in stories:
            # mark story as not realized
            story.realized = False

            # remove rejection comment if it has been rejected before
            story.rejection_comment = comment

            # remove story from sprint
            story.sprint = None

            # save updated story
            story.save()

        return JsonResponse([x[0].api_data for x in stories], safe=False, status=200)
