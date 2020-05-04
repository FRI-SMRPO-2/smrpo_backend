from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from rest_framework.views import APIView

from smrpo.forms import CreateStoryForm
from smrpo.models.project import Project

from smrpo.models.story import Story


class StoriesView(APIView):
    """
        Get all project stories.
    """

    def get(self, request, project_id):
        user = request.user

        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return HttpResponse('Projekt s tem ID-jem ne obstaja', 404)

        # check if user is part of the project
        if not user.is_superuser:
            is_developer = project.developers.all().filter(pk=user.api_data()['id']).exists()
            if not (project.product_owner == user or project.scrum_master == user or is_developer):
                return HttpResponse('User is forbidden to access this resource.', status=403)

        # get all project stories
        stories = Story.objects.filter(project_id=project_id).distinct()

        # divide stories into 3 sections
        realized = stories.filter(realized=True)
        assigned = stories.exclude(realized=True).filter(sprint__start_date__lte=timezone.now(),
                                                         sprint__end_date__gte=timezone.now())
        realized_ids = list(realized.values_list('id', flat=True))
        assigned_ids = list(assigned.values_list('id', flat=True))
        unassigned = stories.exclude(pk__in=realized_ids + assigned_ids)

        return JsonResponse({
            'realized': [story.api_data for story in realized],
            'assigned': [story.api_data for story in assigned],
            'unassigned': [story.api_data for story in unassigned]
        }, safe=False)

    """
        Create a new project story.
        Only a user with Scrum Master or Product Owner role can create new project stories.
    """

    def post(self, request, project_id):
        user = request.user
        data = request.data

        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return HttpResponse('Projekt s tem ID-jem ne obstaja', 404)

        if not user.is_superuser:
            # Only users that are Scrum Masters or Product Owners can create stories.
            if not (project.product_owner == user or project.scrum_master == user):
                return HttpResponse('User is forbidden to access this resource.', status=403)

        data['project'] = project_id
        form = CreateStoryForm(data, user=user)

        if form.is_valid():
            story = form.save()
            return JsonResponse(story.api_data, status=201)

        errors = dict()
        for key, error in form.errors.items():
            errors[key] = list(error)
        return JsonResponse(errors, safe=False, status=400)


class StoryView(APIView):
    def put(self, request, project_id, story_id):
        user = request.user

        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return HttpResponse('Projekt s tem ID-jem ne obstaja', status=404)

        if not user.is_superuser:
            is_developer = project.developers.all().filter(pk=user.api_data()['id']).exists()
            if not (project.product_owner == user or project.scrum_master == user or is_developer):
                return HttpResponse('User is forbidden to access this resource.', status=403)

        # check if story exists in project
        try:
            story = Story.objects.filter(project_id=project_id).get(pk=story_id)
        except Story.DoesNotExist:
            return HttpResponse("Uporabniška zgodba s tem ID-jem ne obstaja", status=404)

        # story must not belong to any sprint
        if story.sprint is not None:
            return HttpResponse("Uporabniška zgodba je del sprinta!", status=400)

        data = request.data
        name = data.get('name')
        text = data.get('text')
        business_value = data.get('business_value')
        realized = data.get('realized')
        time_complexity = data.get('time_complexity')

        if name:
            story.name = name

        if text:
            story.text = text

        if business_value:
            story.business_value = business_value

        if realized:
            story.realized = realized

        # is not None - because 0 is equal to false in Python
        if time_complexity is not None:
            if time_complexity <= 0.0:
                return HttpResponse("Časovna zahtevnost mora biti večja od 0 točk!", status=400)
            if time_complexity > 200:
                return HttpResponse("Časovna zahtevnost ne sme biti večja od 200 točk!", status=400)
            story.time_complexity = time_complexity

        try:
            story.save()
        except:
            return HttpResponse("Napaka pri posodabljanju uporabniške zgodbe!", 500)

        return JsonResponse(story.api_data, safe=False, status=201)
