from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        exclude = ['date_joined', 'password']
        model = User

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        # Set fields as required
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
