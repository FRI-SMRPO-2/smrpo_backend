from django.contrib.auth.models import AbstractUser

from smrpo.models.project import Project


class User(AbstractUser):
    def get_project_roles(self, project_id):
        try:
            project = Project.objects.get(pk=project_id)

            roles = []
            if project.scrum_master == self:
                roles.append("Scrum Master")
            if project.product_owner == self:
                roles.append("Product Owner")
            if project.developers.all().filter(id=self.api_data()['id']).exists():
                roles.append("Developer")

            return roles
        except Project.DoesNotExist:
            return []

    def api_data(self, project_id=None):
        result = dict(
            id=self.id,
            name=self.get_full_name(),
            username=self.username,
            email=self.email,
        )

        if project_id is not None:
            result['role'] = self.get_project_roles(project_id)

        return result
