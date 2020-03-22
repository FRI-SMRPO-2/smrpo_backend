from django.shortcuts import render
from django.views.generic.base import View

from smrpo_backend.models.project import Project


class HomeView(View):
    @staticmethod
    def get(request):
        user = request.user
        context = dict()

        if not user.is_anonymous:
            context["projects"] = Project.objects.all()
            context["user_projects"] = Project.objects.filter(users=user)

        return render(request, "smrpo_backend/home/home.html", context)
