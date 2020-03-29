from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from smrpo.models.project import Project
from smrpo.models.project_user import ProjectUser, ProjectUserRole


class ProjectsView(APIView):
    """
        Return user's projects.
    """

    def get(self, request):
        role = request.GET.get('role')
        user = request.user

        projects = Project.objects.all()

        # Get user's projects, only superuser can view all projects
        if not user.is_superuser:
            projects = projects.filter(users=user)

        # If role parameter was passed return projects that match provided user role.
        if role:
            projects = projects.filter(projectuser__role__title=role)

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
        user_roles = data.get('user_roles')

        # Check if all fields are set and valid
        error = ProjectUserRole.validate_user_roles(user_roles)

        if error:
            return JsonResponse({'message': error}, status=400)

        if not name:
            return JsonResponse({'message': 'Ime ni nastavljeno'}, status=400)

        # Create a project
        try:
            p = Project.objects.create(name=name, created_by=current_user)
        except IntegrityError:
            return JsonResponse({'message': 'Projekt s tem imenom že obstaja'}, status=400)

        try:
            for user_role in user_roles:
                pu = ProjectUser(user_id=user_role['user_id'], role_id=user_role['role_id'], project=p)
                pu.save()
        except Exception as e:
            print(e)  # TODO replace print with logger
            p.delete()
            return JsonResponse({'message': 'Napaka pri dodajanju uporabnikov v projekt'}, status=400)

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
