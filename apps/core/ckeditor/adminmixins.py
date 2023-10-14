from django.contrib import admin
from django.db import models

from .widgets import CKEditorWidget


class CkEditorModelAdminMixin(admin.ModelAdmin):
    ckeditor_fields = '__all__'

    def formfield_for_dbfield(self, db_field, *args, **kwargs):

        if self.ckeditor_fields == '__all__':
            if isinstance(db_field, models.TextField):
                kwargs['widget'] = CKEditorWidget(config_name='admin')
        else:
            if db_field.name in self.ckeditor_fields:
                kwargs['widget'] = CKEditorWidget(config_name='admin')

        return super().formfield_for_dbfield(db_field, *args, **kwargs)
