from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from smrpo.models import User
from smrpo.models.story import Story, StoryTest
from smrpo.models.task import Task


class ChangeUserForm(UserChangeForm):
    class Meta:
        exclude = ['date_joined', 'last_login', 'is_active', 'is_staff']
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        if user.is_superuser:
            user.is_staff = True

        if commit:
            user.save()
        return user


class UserCreateForm(UserCreationForm):
    class Meta:
        exclude = ['date_joined', 'password', 'last_login']
        model = User

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        # Set fields as required
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        if user.is_superuser:
            user.is_staff = True

        if commit:
            user.save()
        return user


class CreateStoryForm(ModelForm):

    class Meta:
        model = Story
        fields = ['name', 'text', 'business_value', 'project', 'priority']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateStoryForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CreateStoryForm, self).save(commit=False)

        if self.user:
            instance.created_by = self.user

        if commit:
            instance.save()
            tests = []
            for test in self.data.get('tests', list()):
                tests.append(StoryTest(text=test, story=instance))

            StoryTest.objects.bulk_create(tests)
        return instance


class CreateTaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'estimated_time', 'story', 'assignee', 'assignee_awaiting', 'assignee_accepted']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateTaskForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CreateTaskForm, self).save(commit=False)

        if self.user:
            instance.created_by = self.user

        if commit:
            instance.save()
        return instance


class UpdateTaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'estimated_time', 'assignee_awaiting']

    def __init__(self, *args, **kwargs):
        super(UpdateTaskForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(UpdateTaskForm, self).save(commit=False)

        if commit:
            instance.save()
        return instance


class UpdateTaskTitleForm(ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description']

    def __init__(self, *args, **kwargs):
        super(UpdateTaskTitleForm, self).__init__(*args, **kwargs)
