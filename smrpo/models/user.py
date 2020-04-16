from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    @property
    def api_data(self):
        return dict(
            id=self.id,
            name=self.get_full_name(),
            username=self.username,
            email=self.email,
        )
