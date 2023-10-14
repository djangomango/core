from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils.helpers.django import get_upload_path, remove_storage_file_if_exists, get_processed_image_as_field_file
from apps.utils.mixins.models.atoms import TimestampMixin, UuidMixin, TitleSlugMixin


class Category(TimestampMixin, TitleSlugMixin, models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ('title',)

    def __str__(self):
        return self.title


class Tag(TimestampMixin, TitleSlugMixin, models.Model):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ('title',)

    def __str__(self):
        return self.title


class FileAttachment(TimestampMixin, UuidMixin, models.Model):
    category = models.ForeignKey(
        Category,
        related_name='file_attachment',
        verbose_name=_('Category'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    tag = models.ManyToManyField(
        Tag,
        blank=True
    )

    name = models.CharField(_('Name'), max_length=255, help_text='Defaults to filename, if left blank.', blank=True, null=True)
    file = models.FileField(_('File'), upload_to=get_upload_path, max_length=255)
    uploaded = models.DateTimeField(_('Uploaded'), auto_now_add=True)

    class Meta:
        verbose_name = "File Attachment"
        verbose_name_plural = "File Attachments"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.file.url


class ImageAttachment(TimestampMixin, UuidMixin, models.Model):
    """
    example params:

    {"size": [40, 30], "prefix": "xxs-", "force_format": "WEBP"}
    {"size": [160, 120], "prefix": "xs-", "force_format": "WEBP"}
    {"size": [480, 360], "prefix": "sm-", "force_format": "WEBP"}
    {"size": [800, 600], "prefix": "md-", "force_format": "WEBP"}
    {"size": [1280, 960], "prefix": "lg-", "force_format": "WEBP"}
    {"size": [1920, 1440], "prefix": "xl-", "force_format": "WEBP"}
    {"size": [2560, 1920], "prefix": "xxl-", "force_format": "WEBP"}
    """

    _stored: dict

    category = models.ForeignKey(
        Category,
        related_name='image_attachment',
        verbose_name=_('Category'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    tag = models.ManyToManyField(
        Tag,
        blank=True
    )

    name = models.CharField(_('Name'), max_length=255, help_text='Defaults to filename, if left blank.', blank=True, null=True)
    image_raw = models.ImageField(_('Image raw'), upload_to=get_upload_path, max_length=255)
    image_out = models.ImageField(_('Image out'), upload_to=get_upload_path, max_length=255)
    alt = models.CharField(_('Alt'), max_length=100, blank=True, null=True)

    params = models.JSONField(_('Params'), blank=True, null=True)
    uploaded = models.DateTimeField(_('Uploaded'), auto_now_add=True)

    class Meta:
        verbose_name = "Image Attachment"
        verbose_name_plural = "Image Attachments"

    def __str__(self):
        return str(self.id)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.params_field = "params"
        self.image_in_field = "image_raw"
        self.image_out_field = "image_out"
        self.remove_stored_on_change = True

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._stored = dict(zip(field_names, values))

        return instance

    def save(self, *args, **kwargs):

        if not self.name:
            self.name = self.image_raw.name

        image_in = getattr(self, self.image_in_field, None)
        params = getattr(self, self.params_field, None)

        stored_image_in = self._stored.pop(self.image_in_field, None) if hasattr(self, '_stored') else None
        stored_params = self._stored.pop(self.params_field, None) if hasattr(self, '_stored') else None

        if image_in != stored_image_in or params != stored_params:
            if hasattr(self, self.image_out_field):
                if image_in and params:
                    image_out = get_processed_image_as_field_file(image_in.file, image_in.name, **params)
                else:
                    image_out = image_in

                setattr(self, self.image_out_field, image_out)

                stored_image_out = self._stored.pop(self.image_out_field, None) if hasattr(self, '_stored') else None

                if not self._state.adding and self.remove_stored_on_change and image_out != stored_image_out and stored_image_out:
                    remove_storage_file_if_exists(stored_image_out)

            if not self._state.adding and self.remove_stored_on_change and image_in != stored_image_in and stored_image_in:
                remove_storage_file_if_exists(stored_image_in)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.image_out.url
