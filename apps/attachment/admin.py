from django.apps import apps
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from apps.attachment.models import ImageAttachment, FileAttachment
from apps.utils.mixins.admin.core import AutoModelAdminMixin


@admin.register(FileAttachment)
class FileAttachmentAdmin(AutoModelAdminMixin, admin.ModelAdmin):
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super(FileAttachmentAdmin, self).get_readonly_fields(request, obj))
        return readonly_fields + ['get_attachment_url']

    def get_attachment_url(self, obj):
        if obj.uuid:
            url = reverse('common:attachment:file', kwargs={'uuid': obj.uuid})
            return format_html('<a href="{}" target="_blank">{}</a>', url, url)

        return None

    get_attachment_url.short_description = "attachment url"


@admin.register(ImageAttachment)
class ImageAttachmentAdmin(AutoModelAdminMixin, admin.ModelAdmin):
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super(ImageAttachmentAdmin, self).get_readonly_fields(request, obj))
        return readonly_fields + ['image_out', 'get_attachment_url']

    def get_attachment_url(self, obj):
        if obj.uuid:
            url = reverse('common:attachment:image', kwargs={'uuid': obj.uuid})
            return format_html('<a href="{}" target="_blank">{}</a>', url, url)

        return None

    get_attachment_url.short_description = "attachment url"


app_config = apps.get_app_config('attachment')

app_config.model_imports()

models = app_config.get_models()
for model in models:
    try:
        admin.site.register(model, AutoModelAdminMixin)
    except admin.sites.AlreadyRegistered:
        pass
