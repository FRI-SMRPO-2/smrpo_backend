from django.contrib import admin

from smrpo_backend.models import task, project, project_member


@admin.register(task.Task)
class TaskAdmin(admin.ModelAdmin):
    list_filter = ('finished', 'closed', 'created', 'updated')
    raw_id_fields = ('created_by', 'finished_by')
    readonly_fields = ('created', 'updated')
    search_fields = ('title',)


class ProjectMembersInline(admin.TabularInline):
    model = project_member.ProjectMember
    extra = 1  # how many rows to show


@admin.register(project.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'created_by', 'deadline', 'finished', 'canceled', 'created', 'updated')
    raw_id_fields = ('created_by',)
    readonly_fields = ('created', 'updated')
    inlines = (ProjectMembersInline,)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            if getattr(obj, 'created_by', None) is None:
                obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(project_member.ProjectMember)
class TaskAdmin(admin.ModelAdmin):
    list_filter = ('created', 'updated')
    raw_id_fields = ('project', 'user')
    readonly_fields = ('created', 'updated')
    search_fields = ('title',)
