from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from smrpo.models.project import Project


class ProjectsView(APIView):
    """
        Return user's projects.
    """

    def get(self, request):
        user = request.user

        if user.is_superuser:
            # Get user's projects, only superuser can view all projects
            projects = Project.objects.all().distinct()
        else:
            # Filter projects so that user can see only their projects
            projects = Project.objects.filter(
                Q(scrum_master=user) | Q(product_owner=user) | Q(developers=user)).distinct()

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
            p = Project.objects.create(
                product_owner_id=product_owner_id,
                scrum_master_id=scrum_master_id,
                name=name,
                created_by=current_user
            )

            p.developers.set(developer_ids)
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
            try:
                project = Project.objects.filter(
                    Q(scrum_master=user) | Q(product_owner=user) | Q(developers=user)).distinct().get(
                    pk=pk)
            except Project.DoesNotExist:
                return HttpResponse("Projekt ne obstaja ali pa uporabnik ni del njega", status=404)

        return JsonResponse(project.api_data, safe=False)

    def put(self, request, pk):
        user = request.user
        data = request.data

        # Check if user is a Scrum Master.
        user_is_scrum_master = Project.objects.filter(
            pk=pk,
            scrum_master=user,
        ).exists()

        if not user.is_superuser and not user_is_scrum_master:
            return HttpResponse('User is forbidden to access this resource.', status=403)

        # check if object exists
        project = get_object_or_404(Project, pk=pk)

        # Extract fields from request
        name = data.get('name')
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

        # Check if there is any new user in the project, if yes, create new work sessions for these users
        # Ugly code ahead
        old_users = set([project.scrum_master_id, project.product_owner_id] + list(project.developers.all().values_list('id', flat=True)))
        new_users = set([scrum_master_id, product_owner_id] + developer_ids)
        users_difference = old_users ^ new_users
        for story in project.stories.filter(sprint__isnull=False):
            for task in story.tasks.all():
                task.create_work_sessions(users_difference)

        if Project.objects.exclude(pk=pk).filter(name=name).exists():
            return HttpResponse("Projekt s tem imenom že obstaja!", status=400)

        try:
            project.name = name
            project.scrum_master_id = scrum_master_id
            project.product_owner_id = product_owner_id
            project.developers.set(developer_ids)
            project.save()
        except:
            return HttpResponse("Napaka pri posodabljanju projekta!", status=500)

        return JsonResponse(project.api_data, safe=False, status=200)


class AuthProjectUserView(APIView):
    """
        Return authenticated project user.
    """

    def get(self, request, pk):
        user = request.user
        return JsonResponse(user.api_data(pk))
