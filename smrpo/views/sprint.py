from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from rest_framework.views import APIView

from smrpo.models.sprint import Sprint


# TODO also add permissions, so that only project memmbers and/or admin can access this API
class SprintsView(APIView):
    """
        Get all project sprints.
    """
    def get(self, request, project_id):
        # Get all project sprints
        sprints = Sprint.objects.filter(project_id=project_id)

        sprints = [sprint.api_data for sprint in sprints]

        return JsonResponse(sprints, safe=False)

    """
        Create new sprint.
    """
    def post(self, request, project_id):
        current_user = request.user
        data = request.data

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
                created_by=current_user
            )
        except ValidationError as e:
            return JsonResponse({'message': str(e)}, status=400)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'message': 'Projekt s tem ID-jem ne obstaja.'}, status=400)
        except Exception as e:
            return JsonResponse({'message': 'Napaka pri dodajanju sprinta.'}, status=400)

        return JsonResponse(s.api_data, safe=False, status=201)


# TODO also add permissions, so that only project memmbers and/or admin can access this API
class SprintView(APIView):
    """
        Get sprint by id.
    """
    def get(self, request, project_id, sprint_id):
        sprint = get_object_or_404(Sprint, id=sprint_id, project_id=project_id)

        return JsonResponse(sprint.api_data, safe=False)
