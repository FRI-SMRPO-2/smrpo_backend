from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from rest_framework.views import APIView

from smrpo.forms import CreateStoryForm
from smrpo.models.project import Project
from smrpo.models.project_user import ProjectUser

from smrpo.models.story import Story


class StoriesView(APIView):
    """
        Get all project stories.
    """

    def get(self, request, project_id):
        user = request.user

        project = Project.objects.filter(id=project_id)
        if not project:
            return HttpResponse('Projekt s tem ID-jem ne obstaja', 404)

        # check if user is part of the project
        if not user.is_superuser:
            try:
                # Check if user is part of the project
                ProjectUser.objects.filter(
                    Q(project_id=project_id),
                    Q(project__scrum_master__user=user) | Q(project__product_owner__user=user) | Q(
                        project__developers__user=user)
                )
            except ProjectUser.DoesNotExist:
                return HttpResponse('User is forbidden to access this resource.', status=403)

        # get all project stories
        stories = Story.objects.filter(project_id=project_id)

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

        if not user.is_superuser:
            # Only users that are Scrum Masters or Product Owners can create stories.
            try:
                # Check if project user can create project stories.
                ProjectUser.objects.get(
                    Q(project_id=project_id),
                    Q(project__scrum_master__user=user) | Q(project__product_owner__user=user)
                )
            except ProjectUser.DoesNotExist:
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
