from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView

from smrpo.forms import CreateStoryForm
from smrpo.models.project_user import ProjectUser


from smrpo.models.story import Story


class StoriesView(APIView):
    """
        Get all project stories.
    """
    def get(self, request, project_id):
        user = request.user
        stories = Story.objects.filter(project_id=project_id)

        if not user.is_superuser:
            stories = stories.filter(
                Q(project__scrum_master__user=user) | Q(project__product_owner__user=user) | Q(project__developers__user=user)
            ).distinct()

        stories = [story.api_data for story in stories]

        return JsonResponse(stories, safe=False)

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
