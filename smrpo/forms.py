from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from smrpo.models.story import Story, StoryTest


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


class CreateStoryForm(ModelForm):

    class Meta:
        model = Story
        fields = ['name', 'text', 'business_value', 'project', 'priority']

    def __init__(self, *args, **kwargs):
        self.project_user = kwargs.pop('project_user', None)
        super(CreateStoryForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CreateStoryForm, self).save(commit=False)

        if self.project_user:
            instance.created_by = self.project_user

        if commit:
            instance.save()
            tests = []
            for test in self.data.get('tests', list()):
                tests.append(StoryTest(text=test, story=instance))

            StoryTest.objects.bulk_create(tests)
        return instance
