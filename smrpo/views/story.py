from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from rest_framework.views import APIView

from smrpo.forms import CreateStoryForm
from smrpo.models.project import Project

from smrpo.models.story import Story, StoryTest


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

        if story.sprint is not None:
            return HttpResponse("Urejaš lahko le zgodbe, ki niso v sprintu.", status=400)

        if story.realized:
            return HttpResponse("Urejaš lahko le nerealizirane zgodbe.", status=400)

        data = request.data
        name = data.get('name')
        text = data.get('text')
        business_value = data.get('business_value')
        realized = data.get('realized')
        time_complexity = data.get('time_complexity')
        priority = data.get('priority')
        tests = data.get('tests', list())

        if not name:
            return HttpResponse("Ime zgodbe ne sme biti prazno.", status=400)
        story.name = name

        if not text:
            return HttpResponse("Opis zgodbe ne sme biti prazen.", status=400)
        story.text = text

        if business_value is None:
            return HttpResponse("Poslovna vrednost zgodbe ne sme biti prazna.", status=400)
        if business_value <= 0:
            return HttpResponse("Poslovna vrednost zgodbe mora biti večja od 0.", status=400)
        if business_value > 10:
            return HttpResponse("Poslovna vrednost zgodbe mora biti manjša od 10.", status=400)

        story.business_value = business_value

        if not priority:
            return HttpResponse("Prioriteta zgodbe ne sme biti prazna.", status=400)
        story.priority_id = priority

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

        if 'tests' in data:
            try:
                # delete all current tests
                StoryTest.objects.filter(story=story).delete()

                if tests is not None:
                    # add new tests
                    new_story_tests = []
                    for test in tests:
                        new_story_tests.append(StoryTest(text=test, story=story))

                    StoryTest.objects.bulk_create(new_story_tests)
            except:
                return HttpResponse("Napaka pri posodabljanju testov!", 500)

        return JsonResponse(story.api_data, safe=False, status=201)

    def delete(self, request, project_id, story_id):
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

        if story.sprint is not None:
            return HttpResponse("Urejaš lahko le zgodbe, ki niso v sprintu.", status=400)

        if story.realized:
            return HttpResponse("Urejaš lahko le nerealizirane zgodbe.", status=400)

        story.delete()
        return JsonResponse({})
