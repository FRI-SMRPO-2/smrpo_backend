import pytz
from django.db.models import Count, Sum
from django.db.models.functions import Trunc
from django.http import JsonResponse, HttpResponse
from django.utils.timezone import now
from rest_framework.views import APIView
from datetime import datetime

from smrpo.models.work_session import WorkSession
import qsstats


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
            date__range=(start_date, end_date)
        )

        # work_sessions.annotate(
        #     day=Trunc('date', 'day')
        # ).values(
        #     'day'
        # ).annotate(
        #     secs=Sum('total_seconds')
        # )

        qss = qsstats.QuerySetStats(work_sessions, 'date', Sum('total_seconds'))
        time_series = qss.time_series(datetime.strptime(start_date, "%Y-%m-%d"), datetime.strptime(end_date, "%Y-%m-%d"))

        return JsonResponse(
            # [t[1]/3600 for t in time_series],
            [[t[0].strftime("%Y-%m-%d"), t[1]/3600] for t in time_series],
            safe=False,
            status=400
        )

    def put(self, request, task_id):
        user = request.user
        data = request.data
        date = data.get('date')
        create_work_session = False

        if not date:
            return HttpResponse('Manjkajoč datum.', status=400)

        date = pytz.utc.localize(datetime.strptime(date, "%Y-%m-%d"))
        if date > now():
            return HttpResponse('Nalog v prihodnosti ne moreš urejati.', status=400)

        try:
            work_session = WorkSession.objects.get(task_id=task_id, user=user, date=date)
        except WorkSession.DoesNotExist:
            # This should not happen?!
            create_work_session = True

        hours = data.get('hours')

        if not hours:
            return HttpResponse('Manjkajoče ure.', status=400)
        if float(hours) < 0:
            return HttpResponse('Ure ne smejo biti negativne.', status=400)

        total_seconds = int(hours * 3600)
        if create_work_session:
            # It should already exist, as it is made when task is made
            work_session = WorkSession.objects.create(
                date=date,
                total_seconds=total_seconds,
                task_id=task_id,
                user=user
            )
        else:
            work_session.total_seconds = total_seconds
            work_session.save()

        return JsonResponse(work_session.api_data)
