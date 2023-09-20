from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from .models import FileData


@admin.register(FileData)
class AdminCSVFileStore(admin.ModelAdmin):
    list_display = ('pk', 'filename')
    search_fields = ('filename',)
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
