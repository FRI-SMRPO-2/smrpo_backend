from django.conf import settings
from django.db import models


class ProjectUserRole(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return "{}".format(self.title)

    @property
    def api_data(self):
        return dict(
            id=self.id,
            title=self.title,
        )

    @staticmethod
    def validate_user_roles(user_roles):
        if not user_roles:
            return 'Podaj seznam uporabnikov.'

        users = set()
        product_owner_role_id = ProjectUserRole.objects.get(title='Product Owner').id
        scrum_master_role_id = ProjectUserRole.objects.get(title='Scrum Master').id

        product_owner_count = 0
        scrum_master_count = 0

        try:
            for user_role in user_roles:
                user_id = user_role.get('user_id')
                role_id = user_role.get('role_id')

                if user_id is None or role_id is None:
                    return 'Neveljaven uporabnik ali vloga.'

                if user_id in users:
                    return 'Uporabnik ima lahko samo eno vlogo.'

                if role_id == product_owner_role_id:
                    product_owner_count += 1

                if role_id == scrum_master_role_id:
                    scrum_master_count += 1

                users.add(user_id)
        except Exception:
            return 'Zgodila se je napaka.'

        if product_owner_count < 1 or product_owner_count > 1:
            return 'V projektu mora biti natanko 1 uporabnik z vlogo Product Owner.'
        if scrum_master_count < 1 or scrum_master_count > 1:
            return 'V projektu mora biti natanko 1 uporabnik z vlogo Scrum Master.'

        return None


class ProjectUser(models.Model):
    """
        Intermediate table for many to many field connecting projects with users.
    """
    role = models.ForeignKey(ProjectUserRole, on_delete=models.PROTECT)

    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('project', 'user')

    def __str__(self):
        return "{} ({})".format(self.user.username, self.role)

    @property
    def api_data(self):
        return dict(
            id=self.id,
            role=self.role.title,
            name=self.user.get_full_name(),
            username=self.user.username,
            email=self.user.email,
        )
