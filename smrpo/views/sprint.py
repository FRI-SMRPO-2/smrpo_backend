from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from rest_framework.views import APIView

from smrpo.models.sprint import Sprint


class SprintsView(APIView):
    """
        Get all sprints (or search by project ID)
    """
    def get(self, request):
        # query parameter
        project = request.GET.get('project')

        # get all sprints
        sprints = Sprint.objects.all()

        if project:
            sprints = sprints.filter(project_id=project)

        sprints = [sprint.api_data for sprint in sprints]

        return JsonResponse(sprints, safe=False)

    """
        Create new sprint
    """
    def post(self, request):
        current_user = request.user
        data = request.data

        start_date = data.get('start_date')
        end_date = data.get('end_date')
        expected_speed = data.get('expected_speed')
        project_id = data.get('project_id')

        if not start_date or not end_date or not expected_speed or not project_id:
            return JsonResponse({'message': 'Nekatera polja niso vnesena'}, status=400)

        # get fields from request
        try:
            start_date = parse_date(data.get('start_date'))
            end_date = parse_date(data.get('end_date'))
            expected_speed = float(data.get('expected_speed'))
            project_id = int(data.get('project_id'))
        except:
            return JsonResponse({'message': 'Eno od polj je v napačnem formatu'}, status=400)

        # insert object into database
        try:
            s = Sprint(start_date=start_date, end_date=end_date, expected_speed=expected_speed, project_id=project_id, created_by=current_user)
            s.save()
        except ValidationError as e:
            return JsonResponse({'message': str(e)}, status=400)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'message': 'Projekt s tem ID-jem ne obstaja'}, status=400)
        except Exception as e:
            return JsonResponse({'message': 'Napaka pri dodajanju sprinta'}, status=400)

        return JsonResponse(s.api_data, safe=False, status=201)
