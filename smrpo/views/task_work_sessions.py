import pytz
from django.http import JsonResponse, HttpResponse
from django.utils.timezone import now
from rest_framework.views import APIView
from datetime import datetime, timedelta

from smrpo.models.work_session import WorkSession


class TaskWorkSessionsView(APIView):

    def get(self, request, task_id):
        user = request.user
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if not start_date or not end_date:
            return HttpResponse('Manjka začetni ali končni datum.', status=400)

        work_sessions = WorkSession.objects.filter(
            task_id=task_id,
            user=user,
        )

        result = dict()
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        while start_date <= end_date:
            ws = work_sessions.filter(date=start_date)
            if ws:
                ws = ws[0]
                result[ws.date.strftime("%Y-%m-%d")] = dict(
                    hours=ws.total_seconds / 3600,
                    estimated_hours=ws.estimated_seconds / 3600
                )
            else:
                result[start_date.strftime("%Y-%m-%d")] = dict(
                    hours= 0.0,
                    estimated_hours=0.0
                )
            start_date += timedelta(days=1)

        return JsonResponse(result)

    def put(self, request, task_id):
        user = request.user
        data = request.data
        date = data.get('date')

        if not date:
            return HttpResponse('Manjkajoč datum.', status=400)

        date = pytz.utc.localize(datetime.strptime(date, "%Y-%m-%d"))
        if date > now():
            return HttpResponse('Nalog v prihodnosti ne moreš urejati.', status=400)

        try:
            work_session = WorkSession.objects.get(task_id=task_id, user=user, date=date)
        except WorkSession.DoesNotExist:
            return HttpResponse('Delovna seja ne obstaja.', status=404)

        hours = data.get('hours')

        if hours is None:
            return HttpResponse('Manjkajoče ure.', status=400)
        if float(hours) < 0:
            return HttpResponse('Ure ne smejo biti negativne.', status=400)

        estimated_hours = data.get('estimated_hours')
        estimated_seconds = 0
        if estimated_hours is not None:
            if float(estimated_hours) < 0:
                return HttpResponse('Ocenjene ure do konca naloge ne smejo biti negativne.', status=400)
            estimated_seconds = int(estimated_hours * 3600)
        else:
            # Get estimated hours from previous work session if exists, else 0
            previous = WorkSession.objects.filter(user=user, task_id=task_id, date__lt=date).last()
            if previous:
                estimated_seconds = previous.estimated_seconds

        total_seconds = int(hours * 3600)
        work_session.total_seconds = total_seconds
        work_session.estimated_seconds = estimated_seconds
        work_session.save()

        return JsonResponse(work_session.api_data)
