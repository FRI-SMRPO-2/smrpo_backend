from django.contrib import admin

from smrpo.models import task, project, project_user, sprint, story


@admin.register(task.Task)
class TaskAdmin(admin.ModelAdmin):
    list_filter = ('finished', 'closed', 'created', 'updated')
    raw_id_fields = ('created_by', 'finished_by')
    readonly_fields = ('created', 'updated')
    search_fields = ('title',)


class ProjectUsersInline(admin.TabularInline):
    model = project_user.ProjectUser
    extra = 1  # how many rows to show


@admin.register(project.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'documentation', 'created_by', 'created', 'updated')
    raw_id_fields = ('created_by',)
    readonly_fields = ('created', 'updated')
    inlines = (ProjectUsersInline,)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            if getattr(obj, 'created_by', None) is None:
                obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(project_user.ProjectUser)
class ProjectUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role', 'created', 'updated')
    list_filter = ('created', 'updated')
    raw_id_fields = ('project', 'user')
    readonly_fields = ('created', 'updated')
    search_fields = ('title',)


@admin.register(project_user.ProjectUserRole)
class ProjectUserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    search_fields = ('title',)


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
    list_display = ('id', 'text')


@admin.register(story.StoryTest)
class StoryTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'story')
    readonly_fields = ('story',)
