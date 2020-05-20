from django.db.models import Count, Sum
from django.db.models.functions import Trunc
from django.http import JsonResponse, HttpResponse
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
