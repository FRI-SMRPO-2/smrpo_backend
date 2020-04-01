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
            stories = stories.filter(project__users=user)

        stories = [story.api_data for story in stories]

        return JsonResponse(stories, safe=False)

    """
        Create a new project story.
        Only a user with methodology master or project manager role can create new project stories.
    """
    def post(self, request, project_id):
        user = request.user
        data = request.data

        if not user.is_superuser:
            # Only users that are methodology masters or project managers can create stories.
            try:
                # Check if project user can create project stories.
                ProjectUser.objects.get(
                    project_id=project_id,
                    user=user,
                    role__title__in=['Methodology master', 'Project manager']
                )
            except ProjectUser.DoesNotExist:
                return HttpResponse('User is forbidden to access this resource.', status=403)

        data['project'] = project_id
        form = CreateStoryForm(data, user=user)

        if form.is_valid():
            print("FORM IS VALID")
            story = form.save()
            return JsonResponse(story.api_data, status=201)

        errors = dict()
        for key, error in form.errors.items():
            errors[key] = list(error)
        return JsonResponse(errors, safe=False, status=400)
