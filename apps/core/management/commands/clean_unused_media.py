# django-unused-media
# https://github.com/akolpakov/django-unused-media
# adpated from 0.2.1

import os
import re
import time

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.validators import EMPTY_VALUES
from django.db import models


def get_all_model_file_fields():
    all_models = apps.get_models()

    fields = []
    for model in all_models:
        for field in model._meta.get_fields():
            if isinstance(field, models.FileField):
                fields.append(field)

    return fields


def get_all_media(exclude=None, minimum_file_age=None):
    if not exclude:
        exclude = []

    media = set()
    initial_time = time.time()

    for root, dirs, files in os.walk(str(settings.MEDIA_ROOT)):

        for name in files:
            path = os.path.abspath(os.path.join(root, name))
            relpath = os.path.relpath(path, settings.MEDIA_ROOT)

            if minimum_file_age:
                file_age = initial_time - os.path.getmtime(path)
                if file_age < minimum_file_age:
                    continue

            for e in exclude:
                if re.match(r'^%s$' % re.escape(e).replace('\\*', '.*'), relpath):
                    break
            else:
                media.add(path)

    return media


def get_used_media():
    media = set()

    for field in get_all_model_file_fields():

        is_null = {
            '%s__isnull' % field.name: True,
        }

        is_empty = {
            '%s' % field.name: '',
        }

        storage = field.storage

        for value in field.model._base_manager \
                .values_list(field.name, flat=True) \
                .exclude(**is_empty).exclude(**is_null):

            if value not in EMPTY_VALUES:
                media.add(storage.path(value))

    return media


def get_unused_media(exclude=None, minimum_file_age=None):
    if not exclude:
        exclude = []

    all_media = get_all_media(exclude, minimum_file_age)
    used_media = get_used_media()

    return all_media - used_media


def remove_media(files):
    for filename in files:
        os.remove(os.path.join(settings.MEDIA_ROOT, filename))


def remove_unused_media():
    remove_media(get_unused_media())


def remove_empty_dirs(path=None):
    if not path:
        path = settings.MEDIA_ROOT

    if not os.path.isdir(path):
        return False

    listdir = [os.path.join(path, filename) for filename in os.listdir(path)]
    if all(list(map(remove_empty_dirs, listdir))):
        os.rmdir(path)
        return True

    return False


class Command(BaseCommand):
    help = "Clean unused media files which have no reference in models"

    # verbosity
    # 0 means silent
    # 1 means normal output (default).
    # 2 means verbose output

    verbosity = 1

    def add_arguments(self, parser):

        parser.add_argument('--noinput', '--no-input',
                            dest='interactive',
                            action='store_false',
                            default=True,
                            help='Do not ask confirmation')

        parser.add_argument('-e', '--exclude',
                            dest='exclude',
                            action='append',
                            default=[],
                            help='Exclude files by mask (only * is supported), can use multiple --exclude')

        parser.add_argument('--minimum-file-age',
                            dest='minimum_file_age',
                            default=60,
                            type=int,
                            help='Skip files younger this age (sec)')

        parser.add_argument('--remove-empty-dirs',
                            dest='remove_empty_dirs',
                            action='store_true',
                            default=False,
                            help='Remove empty dirs after files cleanup')

        parser.add_argument('-n', '--dry-run',
                            dest='dry_run',
                            action='store_true',
                            default=False,
                            help='Dry run without any affect on your data')

    def info(self, message):
        if self.verbosity > 0:
            self.stdout.write(message)

    def debug(self, message):
        if self.verbosity > 1:
            self.stdout.write(message)

    def _show_files_to_delete(self, unused_media):
        self.debug('Files to remove:')

        for f in unused_media:
            self.debug(f)

        self.info('Total files will be removed: {}'.format(len(unused_media)))

    def handle(self, *args, **options):

        if 'verbosity' in options:
            self.verbosity = options['verbosity']

        unused_media = get_unused_media(
            exclude=options.get('exclude'),
            minimum_file_age=options.get('minimum_file_age'),
        )

        if not unused_media:
            self.info('Nothing to delete. Exit')
            return

        if options.get('dry_run'):
            self._show_files_to_delete(unused_media)
            self.info('Dry run. Exit.')
            return

        if options.get('interactive'):
            self._show_files_to_delete(unused_media)

            # ask user
            question = 'Are you sure you want to remove {} unused files? (y/N)'.format(len(unused_media))

            if input(question).upper() != 'Y':
                self.info('Interrupted by user. Exit.')
                return

        for f in unused_media:
            self.debug('Remove %s' % f)
            os.remove(os.path.join(settings.MEDIA_ROOT, f))

        if options.get('remove_empty_dirs'):
            remove_empty_dirs()

        self.info('Done. Total files removed: {}'.format(len(unused_media)))
