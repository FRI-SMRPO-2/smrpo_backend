from django.contrib import admin

from smrpo_backend.models import task, project


@admin.register(task.Task)
class TaskAdmin(admin.ModelAdmin):
    list_filter = ('finished', 'closed', 'created', 'updated')
    raw_id_fields = ('created_by', 'finished_by')
    readonly_fields = ('created', 'updated')
    search_fields = ('title',)


@admin.register(project.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'created_by', 'deadline', 'finished', 'canceled', 'created', 'updated')
    raw_id_fields = ('created_by',)
    readonly_fields = ('created', 'updated')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            if getattr(obj, 'created_by', None) is None:
                obj.created_by = request.user
        super().save_model(request, obj, form, change)
