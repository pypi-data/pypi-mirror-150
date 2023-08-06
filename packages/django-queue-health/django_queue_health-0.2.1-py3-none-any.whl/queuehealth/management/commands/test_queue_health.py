# -*- coding: utf-8 -*-
import logging
import time

from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        m = int(settings.DQH_TRESHOLD)
        treshold = float(m*60)
        str_timestamp = cache.get('DQH_TIMESTAMP')
        if str_timestamp is not None:
            timestamp = float(str_timestamp)
            down_time = time.time() - treshold
            if timestamp < down_time:
                raise CommandError('No queue log in last {} minutes.'
                                   .format(m))
            logger.info('Test passed.')
        else:
            logger.info('No timestamp in cache.')
