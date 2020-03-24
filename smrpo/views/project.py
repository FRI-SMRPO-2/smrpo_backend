from django.db import IntegrityError
from django.http import JsonResponse, Http404, HttpResponseBadRequest, HttpResponse
from rest_framework.views import APIView

from smrpo.models.project import Project
from smrpo.models.project_user import ProjectUser


class ProjectsView(APIView):
    """
        Return user's projects.
    """
    def get(self, request):
        role = request.GET.get('role')
        user = request.user

        # Get user's projects
        projects = Project.objects.filter(users=user)

        # If role parameter was passed return projects that match provided user role.
        if role:
            projects = projects.filter(projectuser__role__title=role)

        projects = [project.api_data for project in projects]

        return JsonResponse(projects, safe=False)

    @staticmethod
    def validate_user_roles_list(user_roles):
        if not user_roles or not isinstance(user_roles, list) or len(user_roles) == 0:
            return 'Podaj seznam uporabnikov'

        users = set()
        for user_role in user_roles:
            if len(user_role) != 2 or 'user_id' not in user_role or 'role_id' not in user_role:
                return 'Ključi v seznamu uporabnikov morajo biti id in role_id'

            if not isinstance(user_role['user_id'], int) or not isinstance(user_role['role_id'], int):
                return 'Ključa id in role_id morata biti števili'

            if user_role['user_id'] in users:
                return 'Uporabnik ima lahko samo eno vlogo'

            users.add(user_role['user_id'])

        return None

    def post(self, request):
        data = request.data
        current_user = request.user

        # extract fields from request
        name = data.get('name')
        user_roles = data.get('user_roles', [])

        # check if all fields are set and valid
        message = self.validate_user_roles_list(user_roles)
        if message is not None:
            return JsonResponse({'message': message}, status=400)

        if not name:
            return JsonResponse({'message': 'Ime ni nastavljeno'}, status=400)

        # create a project
        try:
            p = Project(name=name, created_by=current_user, )
            p.save()
        except IntegrityError:
            return JsonResponse({'message': 'Projekt s tem imenom že obstaja'}, status=400)

        try:
            for user_role in user_roles:
                pu = ProjectUser(user_id=user_role['user_id'], role_id=user_role['role_id'], project_id=p.id)
                pu.save()
        except:
            p.delete()
            return JsonResponse({'message': 'Napaka pri dodajanju uporabnikov v projekt'}, status=400)

        return JsonResponse(p.api_data, safe=False)


class ProjectView(APIView):
    """
        Return user's project by id.
    """
    @staticmethod
    def get_object(pk, user):
        try:
            return Project.objects.get(pk=pk, users=user)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = request.user
        project = self.get_object(pk, user)

        return JsonResponse(project.api_data, safe=False)
