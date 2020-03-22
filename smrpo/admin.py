from django.contrib import admin

from smrpo.models import task, project, project_user


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
    list_display = ('id', 'title', 'description', 'created_by', 'deadline', 'finished', 'canceled', 'created', 'updated')
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
    list_filter = ('created', 'updated')
    raw_id_fields = ('project', 'user')
    readonly_fields = ('created', 'updated')
    search_fields = ('title',)


@admin.register(project_user.ProjectUserRole)
class ProjectUserRoleAdmin(admin.ModelAdmin):
    list_display = ('role', 'description')
    search_fields = ('role', 'description',)
