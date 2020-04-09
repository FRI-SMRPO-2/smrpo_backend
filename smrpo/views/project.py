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
        # These are all user IDs
        scrum_master_id = data.get('scrum_master_id')
        product_owner_id = data.get('product_owner_id')
        developer_ids = data.get('developer_ids')

        if not name:
            return JsonResponse({'message': 'Ime ni nastavljeno'}, status=400)

        if not scrum_master_id:
            return JsonResponse({'message': 'Scrum master ni nastavljen'}, status=400)

        if not product_owner_id:
            return JsonResponse({'message': 'Product owner ni nastavljen'}, status=400)

        if not isinstance(developer_ids, list):
            return JsonResponse({'message': 'Developers mora biti seznam'}, status=400)

        # Remove duplicates from developer list
        developer_ids = list(set(developer_ids))

        # Create a project
        p = None
        try:
            developers = []
            p = Project.objects.create(name=name, created_by=current_user)

            p.product_owner = ProjectUser.objects.create(user_id=product_owner_id, project=p)
            if product_owner_id == scrum_master_id:
                p.scrum_master = p.product_owner
            else:
                p.scrum_master = ProjectUser.objects.create(user_id=scrum_master_id, project=p)

            for developer_id in developer_ids:
                if developer_id == product_owner_id or developer_id == scrum_master_id:
                    developers.append(developer_id)
                else:
                    developers.append(ProjectUser.objects.create(user_id=developer_id, project=p).id)

            p.developers.set(developers)
            p.save()
        except Exception as e:
            if p:
                p.delete()
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
