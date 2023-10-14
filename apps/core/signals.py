from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.core.models import SiteConfig, ConfigGoogleRecaptcha


@receiver(post_save, sender=Site)
def post_save_site(sender, instance, created, **kwargs):
    for obj in instance.site_config.all():
        obj.save()


@receiver(post_save, sender=SiteConfig)
def create_site_config(sender, instance, created, **kwargs):
    if created:
        related_models = [
            ConfigGoogleRecaptcha,
        ]

        for related_model in related_models:
            related_model.objects.create(site_config=instance)


@receiver(post_save, sender=SiteConfig)
def post_save_site_config(sender, instance, created, **kwargs):
    related_objects = [
        'config_google_recaptcha',
    ]

    for related_object in related_objects:
        obj = getattr(instance, related_object, None)

        if obj:
            obj.save()
