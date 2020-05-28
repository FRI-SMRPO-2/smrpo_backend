from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from smrpo.forms import UserCreateForm, ChangeUserForm
from smrpo.models import User
from smrpo.models.task import Task
from smrpo.models.work_session import WorkSession


class UsersView(APIView):
    """
        Return a list of all users.
        Only superuser can access this view.
    """
    def get(self, request):
        # Scrum master is also allowed to search user when editing project
        # if not request.user.is_superuser:
        #    return HttpResponse('User is forbidden to access this resource.', status=403)

        search = request.GET.get('search')

        # Get users
        users = User.objects.all()

        if search:
            users = users.filter(
                Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(username__icontains=search) | Q(email__icontains=search)
            )

        users_list = []
        for user in users:
            users_list.append(dict(
                id=user.id,
                name=user.get_full_name(),
                username=user.username,
                email=user.email
            ))

        return JsonResponse(users_list, safe=False)

    def post(self, request):
        if not request.user.is_superuser:
            return HttpResponse('Samo administrator lahko ustvarja nove račune.', status=403)

        form = UserCreateForm(request.data)
        if form.is_valid():
            user = form.save()
            return JsonResponse(
                dict(
                    id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    full_name=user.get_full_name(),
                    username=user.username,
                    email=user.email,
                    last_login=user.last_login,
                    is_superuser=user.is_superuser
                ),
                status=201
            )

        errors = dict()
        for key, error in form.errors.items():
            errors[key] = list(error)

        return JsonResponse(errors, status=400)


class UpdateUserView(APIView):
    """
        Only superuser can access this view.
    """
    def get(self, request, user_id):
        if not request.user.is_superuser:
            return HttpResponse('Samo administrator lahko dostopa do vseh uporabnikov.', status=403)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponse('Uporabnik, ki ga želiš urejati ne obstaja.', status=404)

        return JsonResponse(dict(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            full_name=user.get_full_name(),
            username=user.username,
            email=user.email,
            last_login=user.last_login,
            is_superuser=user.is_superuser
        ))

    def put(self, request, user_id):
        if not request.user.is_superuser:
            return HttpResponse('Samo administrator sistema lahko ureja račune.', status=403)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponse('Uporabnik, ki ga želiš urejati ne obstaja.', status=404)

        form = ChangeUserForm(request.data, instance=user)
        if form.is_valid():
            pw1 = request.data.get('password1')
            pw2 = request.data.get('password2')
            if pw1 or pw2:
                pass_form = SetPasswordForm(user=user, data=dict(new_password1=pw1, new_password2=pw2))
                if pass_form.is_valid():
                    pass_form.save()
                else:
                    errors = dict()
                    for key, error in pass_form.errors.items():
                        errors[key] = list(error)
                    return JsonResponse(errors, safe=False, status=400)

            user = form.save()

            return JsonResponse(dict(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                full_name=user.get_full_name(),
                username=user.username,
                email=user.email,
                last_login=user.last_login,
                is_superuser=user.is_superuser
            ))

        errors = dict()
        for key, error in form.errors.items():
            errors[key] = list(error)
        return JsonResponse(errors, safe=False, status=400)

    def delete(self, request, user_id):
        if not request.user.is_superuser:
            return HttpResponse('Samo administrator sistema lahko briše račune.', status=403)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponse('Uporabnik, ki ga želiš izbrisati ne obstaja.', status=404)

        Task.objects.filter(Q(assignee=user) | Q(assignee_awaiting=user)).update(
            assignee=None,
            assignee_awaiting=None,
            assignee_accepted=None
        )

        WorkSession.objects.filter(user=user).delete()

        user.delete()

        return JsonResponse(dict(), status=200)


class AuthUserInfoView(APIView):
    """
        Return authenticated user's info.
    """
    def get(self, request):
        user = request.user

        return JsonResponse(dict(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                full_name=user.get_full_name(),
                username=user.username,
                email=user.email,
                last_login=user.last_login,
                is_superuser=user.is_superuser
            )
        )

    def put(self, request):
        """
            Update authenticated user's data.
        """
        user = request.user

        form = ChangeUserForm(request.data, exclude_is_superuser=True, instance=user)
        if form.is_valid():
            pw1 = request.data.get('password1')
            pw2 = request.data.get('password2')
            if pw1 or pw2:
                pass_form = SetPasswordForm(user=user, data=dict(new_password1=pw1, new_password2=pw2))
                if pass_form.is_valid():
                    pass_form.save()
                else:
                    errors = dict()
                    for key, error in pass_form.errors.items():
                        errors[key] = list(error)
                    return JsonResponse(errors, safe=False, status=400)

            user = form.save()

            return JsonResponse(dict(
                    id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    full_name=user.get_full_name(),
                    username=user.username,
                    email=user.email,
                    last_login=user.last_login,
                    is_superuser=user.is_superuser
                )
            )

        errors = dict()
        for key, error in form.errors.items():
            errors[key] = list(error)
        return JsonResponse(errors, safe=False, status=400)


class AuthUserTasksView(APIView):
    """
        Return authenticated user's assigned tasks.
    """
    def get(self, request):
        user = request.user

        return JsonResponse(dict(
                assigned_tasks=[t.api_data for t in user.assignee.all()],
                assignee_awaiting_tasks=[t.api_data for t in user.assignee_awaiting.all()]
            )
        )

