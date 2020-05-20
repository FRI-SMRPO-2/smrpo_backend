from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from smrpo.models import task, project, sprint, story, post, User, work_session


@admin.register(task.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'estimated_time', 'story', 'created_by', 'created', 'updated')
    list_filter = ('finished', 'created', 'updated')
    raw_id_fields = ('created_by', 'finished_by')
    readonly_fields = ('created', 'updated')
    search_fields = ('title',)


@admin.register(work_session.WorkSession)
class WorkSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'task', 'date', 'active', 'total_seconds', 'created', 'updated')
    list_filter = ('date', 'active', 'created', 'updated')
    raw_id_fields = ('task', 'user')
    readonly_fields = ('created', 'updated')
    search_fields = ('user__username', 'task__title')


class ProjectSprintsInline(admin.TabularInline):
    model = sprint.Sprint
    extra = 1  # how many rows to show


class ProjectStoriesInline(admin.TabularInline):
    model = story.Story
    extra = 1  # how many rows to show


@admin.register(project.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'documentation', 'created_by', 'created', 'updated')
    raw_id_fields = ('created_by',)
    readonly_fields = ('created', 'updated')
    inlines = (ProjectSprintsInline, ProjectStoriesInline)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            if getattr(obj, 'created_by', None) is None:
                obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(sprint.Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_date', 'end_date', 'expected_speed', 'project',)
    search_fields = ('start_date', 'end_date', 'expected_speed', 'project',)


@admin.register(story.Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'text', 'business_value', 'project', 'priority', 'created_by', 'created', 'updated')
    raw_id_fields = ('project', 'created_by',)
    readonly_fields = ('created', 'updated')


@admin.register(story.StoryPriority)
class StoryPriorityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(story.StoryTest)
class StoryTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'story')
    readonly_fields = ('story',)


@admin.register(post.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')

class CustomUserAdmin(UserAdmin):
    model = User


admin.site.register(User, CustomUserAdmin)
