from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from smrpo.forms import UserCreateForm


class UsersView(APIView):
    """
        Return a list of all users.
    """
    def get(self, request):
        # TODO only admin and methodology master can access this view
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
            return HttpResponse('User is forbidden to access this resource.', status=403)

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
