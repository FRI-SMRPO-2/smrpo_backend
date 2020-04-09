from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from smrpo.models.project import Project
from smrpo.models.project_user import ProjectUser


class ProjectsView(APIView):
    """
        Return user's projects.
    """

    def get(self, request):
        user = request.user

        projects = Project.objects.all()

        # Get user's projects, only superuser can view all projects
        if not user.is_superuser:
            # Filter projects so that user can see only their projects
            projects = projects.filter(users=user)

        if request.GET.get('names'):
            projects = list(projects.values('id', 'name'))
        else:
            projects = [project.api_data for project in projects]

        return JsonResponse(projects, safe=False)

    def post(self, request):
        current_user = request.user
        if not current_user.is_superuser:
            return HttpResponse('User is forbidden to access this resource.', status=403)

        data = request.data

        # Extract fields from request
        name = data.get('name')
        scrum_master = data.get('scrum_master')
        product_owner = data.get('product_owner')
        developers = data.get('developers')

        if not name:
            return JsonResponse({'message': 'Ime ni nastavljeno'}, status=400)

        if not scrum_master:
            return JsonResponse({'message': 'Scrum master ni nastavljen'}, status=400)

        if not product_owner:
            return JsonResponse({'message': 'Product owner ni nastavljen'}, status=400)

        if not isinstance(developers, list):
            return JsonResponse({'message': 'Developers mora biti seznam'}, status=400)

        # Create a project
        try:
            p = Project.objects.create(name=name, created_by=current_user, scrum_master_id=scrum_master, product_owner_id=product_owner)
            p.developers.set(developers)
        except Exception as e:
            return JsonResponse({'message': 'Napaka pri dodajanju projekta'}, status=400)

        return JsonResponse(p.api_data, safe=False, status=201)


class ProjectView(APIView):
    """
        Return user's project by id.
    """
    def get(self, request, pk):
        user = request.user
        # Check if user is superuser or if user is project user.
        if user.is_superuser:
            project = get_object_or_404(Project, pk=pk)
        else:
            project = get_object_or_404(Project, pk=pk, users=user)

        return JsonResponse(project.api_data, safe=False)


class AuthProjectUserView(APIView):
    """
        Return authenticated project user.
    """

    def get(self, request, pk):
        project_user = get_object_or_404(ProjectUser, user=request.user, project_id=pk)
        return JsonResponse(project_user.api_data)
