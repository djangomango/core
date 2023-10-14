import json
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management import BaseCommand

from apps.core.models import SiteConfig, NavigationLink, ConfigGoogleRecaptcha
from apps.utils.helpers.django import get_object_or_none


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('\n adding user model entries')

        superusers_path = os.path.join(settings.BASE_DIR, 'superusers.json')
        with open(superusers_path) as f:
            superusers = json.load(f)

        for superuser in superusers:
            username = superuser.get('username', 'user')
            email = superuser.get('email', 'user@domain.com')
            password = superuser.get('password', 'pass1234')

            user = get_object_or_none(get_user_model(), **{'username': username})
            if not user:
                user = get_user_model().objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )

            user.first_name = superuser.get('first_name', None)
            user.last_name = superuser.get('last_name', None)

            user.save()


        #######################################################################
        # site

        print('\n adding site')

        site = Site.objects.get(id=1)

        site.name = settings.DJANGO_SITE_NAME
        site.domain = settings.DJANGO_SITE_DOMAIN

        site.save()

        #######################################################################
        # configuration

        print('\n adding configuration')

        site_config = SiteConfig.objects.filter(site=site).last()

        if not site_config:
            site_config = SiteConfig.objects.create(site=site)

        site_config.site_description = """
DjangoMango offers pre-built themes and web apps built on Django. Our products are built following coding best-practices, 
based on modular design, using the latest frameworks, all packaged up on ready-to-run docker images.
"""

        site_config.is_active = True

        site_config.save()

        #######################################################################
        # navigation menu links

        print('\n adding navigation menu links')

        nav_items = [
            {'order': 0, 'title': 'Home', 'target': '/', 'featured': False},
        ]

        NavigationLink.objects.all().delete()

        for count, item in enumerate(nav_items):
            NavigationLink.objects.update_or_create(
                pk=count + 1,
                site_config=site_config,
                defaults={**item}
            )

        #######################################################################
        # google recaptcha

        print('\n adding google recaptcha')

        dic = {
            'is_active': settings.GOOGLE_RECAPTCHA_IS_ACTIVE or False,
            'site_key': settings.GOOGLE_RECAPTCHA_SITE_KEY,
            'secret_key': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        }

        ConfigGoogleRecaptcha.objects.update_or_create(
            site_config=site_config,
            defaults={**dic}
        )
