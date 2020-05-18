from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from smrpo.models.post import Post
from smrpo.models.project import Project


class PostView(APIView):
    """
        Add post to project
    """
    def post(self, request, project_id):
        user = request.user
        data = request.data

        # get project
        project = get_object_or_404(Project, pk=project_id)

        # check if user is part of the project
        if not user.is_superuser:
            is_developer = project.developers.all().filter(pk=user.api_data()['id']).exists()
            if not (project.product_owner == user or project.scrum_master == user or is_developer):
                return HttpResponse('User is forbidden to access this resource.', status=403)

        text = data.get('text')

        if not text:
            return HttpResponse("Besedilo ni podano", status=400)

        try:
            post = Post()
            post.text = text
            post.created_by = user
            post.project = project
            post.save()
        except:
            return HttpResponse("Napaka pri dodajanju objave", status=500)

        return JsonResponse(project.api_data, safe=False, status=201)
