from django.contrib.sites.models import Site
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils.mixins.models.atoms import TimestampMixin, TitleMixin, OrderMixin


class SiteConfig(TimestampMixin, models.Model):
    site = models.ForeignKey(
        Site,
        related_name='site_config',
        verbose_name=_('Site'),
        on_delete=models.CASCADE
    )

    is_active = models.BooleanField(_('Is active?'), default=False)
    site_description = models.TextField(_('Site description'), max_length=255, blank=True, null=True)
    maintenance_mode = models.BooleanField(_('Maintenance mode?'), default=False)
    auth_required = models.BooleanField(_('Authentication required?'), default=False)

    class Meta:
        verbose_name = "Site Config"
        verbose_name_plural = "Site Config"

    def __str__(self):
        return self.site.name


class NavigationLink(TimestampMixin, OrderMixin, TitleMixin, models.Model):
    site_config = models.ForeignKey(
        SiteConfig,
        related_name='navigation_link',
        verbose_name=_('Site Config'),
        on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='child',
        blank=True,
        null=True
    )

    target = models.CharField(_('Target'), max_length=255)
    extra = models.CharField(_('Extra'), max_length=255, blank=True, null=True)
    show = models.BooleanField(_('Show?'), default=True)
    featured = models.BooleanField(_('Featured?'), default=False)

    class Meta:
        verbose_name = "Navigation Link"
        verbose_name_plural = "Navigation Links"
        ordering = ('order',)

    def __str__(self):
        return self.title


class ConfigGoogleRecaptcha(TimestampMixin, models.Model):
    min_validator = MinValueValidator(0.0)
    max_validator = MaxValueValidator(1.0)

    site_config = models.OneToOneField(
        SiteConfig,
        related_name='config_google_recaptcha',
        verbose_name=_('Site Config'),
        on_delete=models.CASCADE
    )

    is_active = models.BooleanField(_('Is active?'), default=False)
    site_key = models.CharField(_('Site key'), max_length=255, blank=True, null=True)
    secret_key = models.CharField(_('Secret key'), max_length=255, blank=True, null=True)
    threshold = models.FloatField(_('Threshold'), validators=[min_validator, max_validator], default=0.5)

    class Meta:
        verbose_name = "Config Google reCAPTCHA"
        verbose_name_plural = "Config Google reCAPTCHA"

    def __str__(self):
        return self.site_config.site.name
