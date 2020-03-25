from django.db import IntegrityError
from django.http import JsonResponse, Http404, HttpResponse
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
        if not user_roles:
            return 'Podaj seznam uporabnikov.'

        users = set()
        try:
            for user_role in user_roles:
                user_id = user_role.get('user_id')
                role_id = user_role.get('role_id')
                if user_id is None or role_id is None:
                    return 'Neveljaven uporabnik ali vloga.'

                if user_id in users:
                    return 'Uporabnik ima lahko samo eno vlogo.'

                users.add(user_id)
        except Exception as e:
            print(e)  # TODO replace print with logger
            return 'Zgodila se je napaka.'

        return None

    def post(self, request):
        current_user = request.user
        if not current_user.is_superuser:
            return HttpResponse('User unauthorized.', status=401)

        data = request.data

        # Extract fields from request
        name = data.get('name')
        user_roles = data.get('user_roles')

        # Check if all fields are set and valid
        error = self.validate_user_roles_list(user_roles)

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
