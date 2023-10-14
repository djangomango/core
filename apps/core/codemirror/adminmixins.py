from django.contrib import admin
from django.db import models

from .widgets import CodeMirrorEditor


class CodeMirrorModelAdminMixin(admin.ModelAdmin):
    codemirror_fields = '__all__'

    def formfield_for_dbfield(self, db_field, *args, **kwargs):

        if self.codemirror_fields == '__all__':
            if isinstance(db_field, models.TextField):
                kwargs['widget'] = CodeMirrorEditor()
        else:
            if db_field.name in self.codemirror_fields:
                kwargs['widget'] = CodeMirrorEditor()

        return super().formfield_for_dbfield(db_field, *args, **kwargs)
