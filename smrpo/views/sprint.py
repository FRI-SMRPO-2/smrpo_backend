from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_date
from rest_framework.views import APIView

from smrpo.models.project import Project
from smrpo.models.sprint import Sprint


class SprintsView(APIView):
    """
        Get all project sprints.
    """
    def get(self, request, project_id):
        user = request.user
        # Get all project sprints
        sprints = Sprint.objects.filter(project_id=project_id)

        # Get project's sprints, only superuser can view all sprints
        if not user.is_superuser:
            sprints = sprints.filter(Q(project__scrum_master=user) | Q(project__product_owner=user) | Q(project__developers=user)).distinct()

        sprints = [sprint.api_data for sprint in sprints]

        return JsonResponse(sprints, safe=False)

    """
        Create a new sprint.
        Only superuser or project user with the Scrum Master role can create new sprints.
    """
    def post(self, request, project_id):
        user = request.user
        data = request.data

        # Check if user is a Scrum Master.
        user_is_scrum_master = Project.objects.filter(
            id=project_id,
            scrum_master=user,
        ).exists()

        if not user.is_superuser and not user_is_scrum_master:
            return HttpResponse('User is forbidden to access this resource.', status=403)

        start_date = data.get('start_date')
        end_date = data.get('end_date')
        expected_speed = data.get('expected_speed')

        if not start_date or not end_date or not expected_speed:
            return JsonResponse({'message': 'Nekatera polja niso vnesena.'}, status=400)

        # Get fields from request
        try:
            start_date = parse_date(data.get('start_date'))
            end_date = parse_date(data.get('end_date'))
            expected_speed = float(data.get('expected_speed'))
        except:
            return JsonResponse({'message': 'Eno od polj je v napačnem formatu.'}, status=400)

        # Create Sprint
        try:
            s = Sprint.objects.create(
                start_date=start_date,
                end_date=end_date,
                expected_speed=expected_speed,
                project_id=project_id,
                created_by=user
            )
        except ValidationError as e:
            return JsonResponse({'message': e.message}, status=400)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'message': 'Projekt s tem ID-jem ne obstaja.'}, status=400)
        except Exception as e:
            return JsonResponse({'message': 'Napaka pri dodajanju sprinta.'}, status=400)

        return JsonResponse(s.api_data, safe=False, status=201)


class SprintView(APIView):
    """
        Get sprint by id.
    """
    def get(self, request, project_id, sprint_id):
        user = request.user

        # Check if user is superuser or if user is project user.
        if user.is_superuser:
            sprint = get_object_or_404(Sprint, id=sprint_id, project_id=project_id)
        else:
            try:
                sprint = Sprint.objects.filter(project_id=project_id).filter(
                    Q(project__product_owner=user) | Q(project__scrum_master=user) | Q(project__developers=user)).get(
                    pk=sprint_id)
            except Sprint.DoesNotExist:
                return HttpResponse("Sprint ne obstaja", status=404)

        return JsonResponse(sprint.api_data, safe=False)
    
    def put(self, request, project_id, sprint_id):
        user = request.user
        data = request.data

        # Check if user is a Scrum Master.
        user_is_scrum_master = Project.objects.filter(
            id=project_id,
            scrum_master=user,
        ).exists()

        if not user.is_superuser and not user_is_scrum_master:
            return HttpResponse('User is forbidden to access this resource.', status=403)

        # get sprint
        sprint = get_object_or_404(Sprint, pk=sprint_id, project_id=project_id)

        start_date = data.get('start_date')
        end_date = data.get('end_date')
        expected_speed = data.get('expected_speed')

        if not start_date or not end_date or not expected_speed:
            return JsonResponse({'message': 'Nekatera polja niso vnesena.'}, status=400)

        # Get fields from request
        try:
            start_date = parse_date(data.get('start_date'))
            end_date = parse_date(data.get('end_date'))
            expected_speed = float(data.get('expected_speed'))
        except:
            return JsonResponse({'message': 'Eno od polj je v napačnem formatu.'}, status=400)

        if sprint.end_date < timezone.now().date():
            return JsonResponse({'message': 'Sprint je že končan.'}, status=400)

        if sprint.start_date <= timezone.now().date() and (
                sprint.start_date != start_date or sprint.end_date != end_date):
            return JsonResponse({'message': 'Sprememba datuma je dovoljena samo za sprinte, ki se še niso pričeli.'},
                                status=400)

        # update sprint
        try:
            sprint.start_date = start_date
            sprint.end_date = end_date
            sprint.expected_speed = expected_speed
            sprint.save()
        except ValidationError as e:
            return JsonResponse({'message': e.message}, status=400)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'message': 'Projekt s tem ID-jem ne obstaja.'}, status=400)
        except Exception as e:
            return JsonResponse({'message': 'Napaka pri dodajanju sprinta.'}, status=400)

        return JsonResponse(sprint.api_data, safe=False, status=200)

    def delete(self, request, project_id, sprint_id):
        user = request.user

        # Check if user is a Scrum Master.
        user_is_scrum_master = Project.objects.filter(
            id=project_id,
            scrum_master=user,
        ).exists()

        if not user.is_superuser and not user_is_scrum_master:
            return HttpResponse('User is forbidden to access this resource.', status=403)

        # get sprint
        sprint = get_object_or_404(Sprint, pk=sprint_id, project_id=project_id)

        if sprint.start_date <= timezone.now().date():
            return HttpResponse("Sprint je v teku ali se je že končal!", status=400)

        sprint.delete()

        return HttpResponse(status=204)
