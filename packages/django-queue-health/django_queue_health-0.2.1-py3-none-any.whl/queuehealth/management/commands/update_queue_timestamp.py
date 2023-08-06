# -*- coding: utf-8 -*-
import logging
import time

from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--engine', choices=['django_rq', 'celery'],
            default='django_rq',
            help='app which used for queue django_rq(default) / celery',
        )

    def handle(self, *args, **options):
        if options['engine'] == 'django_rq':
            import django_rq
            django_rq.enqueue(set_timestamp)
        elif options['engine'] == 'celery':
            from celery import shared_task

            @shared_task
            def task():
                set_timestamp()


def set_timestamp():
    if settings.DQH_TRESHOLD is None:
        CommandError('DQH_TRESHOLD not specified in settings.')
    m = int(settings.DQH_TRESHOLD)
    timestamp = time.time()
    cache.set(key='DQH_TIMESTAMP', value=str(timestamp), timeout=m * 60 * 6)
    logger.info('Set timestamp {} in cache'.format(timestamp))
