from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView

from smrpo.forms import CreateTaskForm
from smrpo.models.project import Project
from smrpo.models.story import Story
from smrpo.models.task import Task


class StoryTasksView(APIView):

    """
        Create a new task on an active sprint story.
        Only scrum master or developers or super user can create new tasks.
    """
    def post(self, request, story_id):
        user = request.user
        data = request.data

        try:
            story = Story.objects.get(pk=story_id)
        except Project.DoesNotExist:
            return HttpResponse('Zgodba s tem ID-jem ne obstaja', 404)

        if not story.sprint or not story.sprint.is_active:
            return HttpResponse('Nalogo lahko dodaš le zgodbi aktivnega sprinta.', 400)

        if story.realized:
            return HttpResponse('Zgodba je že realizirana, zato ji naloge ni mogoče dodati.', 400)

        if not user.is_superuser:
            if not (story.sprint.project.scrum_master == user or not story.sprint.project.developers.filter(pk=user.id).exists()):
                return HttpResponse(
                    'Samo skrbnik metodlogije, člani razvojne skupine ali administrator lahko dodajajo naloge zgodbam aktivnega sprinta.',
                    status=403
                )

        if data.get('estimated_time'):
            try:
                if data.get('estimated_time') <= 0:
                    return HttpResponse('Časovna zahtevnost naloge mora biti večja od 0 ur.', status=400)
                if data.get('estimated_time') > 200:
                    return HttpResponse('Časovna zahtevnost naloge ne sme biti večja od 200 ur.', status=400)
            except:
                return HttpResponse('Časovna zahtevnost naloge mora biti med 0 in 200 ur.', status=400)

        # If assignee awaiting is current user, then make assignee accepted
        asignee_awaiting_id = data.get('assignee_awaiting_id')
        if asignee_awaiting_id:
            if Project.objects.filter(pk=story.sprint.project_id, developers=asignee_awaiting_id).exists():
                # TODO this code is in case they say, that if assignee selects himself as the assignee_awaiting that it counts as accepted
                # if asignee_awaiting_id == user.id:
                #     data['assignee'] = user
                #     # TODO some time counter should also start as the user has accepted this task
                #     data['assignee_accepted'] = now()
                # else:
                #     data['assignee_awaiting'] = asignee_awaiting_id
                data['assignee_awaiting'] = asignee_awaiting_id
            else:
                return HttpResponse('Izbrani član, kateremu je bila dodeljena naloga, ni del razvojne ekipe.', 400)

        data['story'] = story_id

        form = CreateTaskForm(data, user=user)

        if form.is_valid():
            task = form.save()
            return JsonResponse(task.api_data, status=201)

        errors = dict()
        for key, error in form.errors.items():
            errors[key] = list(error)
        return JsonResponse(errors, safe=False, status=400)


class FinishTaskView(APIView):
    """
        Finish task
    """
    def put(self, request, task_id):
        user = request.user

        # check if user can access this task
        try:
            if user.is_superuser:
                task = Task.objects.get(pk=task_id)
            else:
                task = Task.objects.get(pk=task_id, story__project__developers=user)
        except Task.DoesNotExist:
            return HttpResponse(
                "Naloga z ID-jem {0} ne obstaja ali pa uporabnik nima pravic za dostop".format(str(task_id)),
                status=404)

        if task.finished:
            return HttpResponse("Naloga je že zaključena", status=400)

        # Stop work session
        result = task.finish(user)
        if result:
            return HttpResponse(result, status=400)

        return JsonResponse(task.api_data)


class AcceptTaskView(APIView):
    """
        Accept task
    """
    def put(self, request, task_id):
        user = request.user

        # check if user can access this task
        try:
            task = Task.objects.get(pk=task_id, story__project__developers=user)
        except Task.DoesNotExist:
            return HttpResponse("Naloga ne obstaja ali pa uporabnik nima pravic za dostop.", status=404)

        error = task.accept(user)
        if error:
            return HttpResponse(error, status=400)

        return JsonResponse(task.api_data)


class DeclineTaskView(APIView):
    """
        Decline task
    """
    def put(self, request, task_id):
        user = request.user

        # check if user can access this task
        try:
            task = Task.objects.get(pk=task_id, story__project__developers=user)
        except Task.DoesNotExist:
            return HttpResponse("Naloga ne obstaja ali pa uporabnik nima pravic za dostop.", status=404)

        error = task.decline(user)
        if error:
            return HttpResponse(error, status=400)

        return JsonResponse(task.api_data)


class StartWorkTaskView(APIView):
    """
        Start working on a task
    """
    def put(self, request, task_id):
        user = request.user

        # check if user can access this task
        try:
            task = Task.objects.get(pk=task_id, assignee=user)
        except Task.DoesNotExist:
            return HttpResponse("Naloga ne obstaja ali pa uporabnik ni določen za delo na njej.", status=404)

        error = task.start_work_session()
        if error:
            return HttpResponse(error, status=400)

        return JsonResponse(task.api_data)


class StopWorkTaskView(APIView):
    """
        Stop working on a task
    """
    def put(self, request, task_id):
        user = request.user

        # check if user can access this task
        try:
            task = Task.objects.get(pk=task_id, assignee=user)
        except Task.DoesNotExist:
            return HttpResponse("Naloga ne obstaja ali pa uporabnik ni določen za delo na njej.", status=404)

        # Get assignee work session and stop it
        active_work_session = task.assignee_work_session
        if not active_work_session:
            return HttpResponse("Na nalogi trenutno delo ne poteka, zato dela ni mogoče zaključiti.", status=400)

        active_work_session.stop_work()
        return JsonResponse(task.api_data)


'''
def put(self, request, task_id):
    user = request.user

    # check if user can access this task
    try:
        if user.is_superuser:
            task = Task.objects.get(pk=task_id)
        else:
            task = Task.objects.get(pk=task_id, story__project__developers=user)
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
'''