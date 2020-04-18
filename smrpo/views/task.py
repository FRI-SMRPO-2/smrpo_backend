from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView

from smrpo.models.project import Project
from smrpo.models.task import Task


class TaskView(APIView):
    """
        Modify task
    """
    def put(self, request, task_id):
        user = request.user

        # check if user can access this task
        try:
            if user.is_superuser:
                task = Task.objects.get(pk=task_id)
            else:
                task = Task.objects.filter(
                    Q(story__project__scrum_master=user) | Q(story__project__product_owner=user) | Q(
                        story__project__developers=user)).distinct().get(pk=task_id)
        except Task.DoesNotExist:
            return HttpResponse(
                "Naloga z ID-jem {0} ne obstaja ali pa uporabnik nima pravic za dostop".format(str(task_id)),
                status=404)

        data = request.data
        title = data.get('title')
        assignee_id = data.get('assignee_id')
        finished = data.get('finished')

        if title:
            task.title = title

        if assignee_id:
            # check if assignee is part of the current project
            try:
                # try to get project
                Project.objects.filter(Q(scrum_master_id=assignee_id) | Q(product_owner_id=assignee_id) | Q(
                    developers=assignee_id)).distinct().get(sprints__stories__tasks=task_id)
                task.assignee_id = assignee_id
            except Project.DoesNotExist:
                return HttpResponse("Napaka pri posodabljanju assignee-ja")

        if finished:
            if task.finished:
                return HttpResponse("Naloga je že zaključena", status=400)

            result = task.finish(user)
            if result:
                return HttpResponse(result, status=400)

        # save task updated task to database
        task.save()

        return JsonResponse(task.api_data, safe=False)
