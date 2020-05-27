import pytz
from django.db.models import Count, Sum
from django.db.models.functions import Trunc
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
        # create_work_session = False

        if not date:
            return HttpResponse('Manjkajoč datum.', status=400)

        date = pytz.utc.localize(datetime.strptime(date, "%Y-%m-%d"))
        if date > now():
            return HttpResponse('Nalog v prihodnosti ne moreš urejati.', status=400)

        try:
            work_session = WorkSession.objects.get(task_id=task_id, user=user, date=date)
        except WorkSession.DoesNotExist:
            # This should not happen?!
            # create_work_session = True
            return HttpResponse('Delovna seja ne obstaja.', status=404)

        hours = data.get('hours')

        if not hours:
            return HttpResponse('Manjkajoče ure.', status=400)
        if float(hours) < 0:
            return HttpResponse('Ure ne smejo biti negativne.', status=400)

        estimated_hours = data.get('estimated_hours')
        estimated_seconds = 0
        if estimated_hours:
            estimated_seconds = int(estimated_hours * 3600)
        else:
            # Get estimated hours from previous work session if exists, else 0
            previous = WorkSession.objects.filter(user=user, task_id=task_id, date__lt=date).last()
            if previous:
                estimated_seconds = previous.estimated_seconds

        total_seconds = int(hours * 3600)
        # if create_work_session:
        #     # It should already exist, as it is made when task is made
        #     work_session = WorkSession.objects.create(
        #         date=date,
        #         total_seconds=total_seconds,
        #         estimated_seconds=estimated_seconds,
        #         task_id=task_id,
        #         user=user
        #     )
        # else:
        work_session.total_seconds = total_seconds
        work_session.estimated_seconds = estimated_seconds
        work_session.save()

        return JsonResponse(work_session.api_data)
