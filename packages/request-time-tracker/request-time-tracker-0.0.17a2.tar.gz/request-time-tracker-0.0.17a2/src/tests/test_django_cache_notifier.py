from datetime import datetime, timedelta
from functools import partial

from django.core.cache import caches
from django.test import TestCase

from freezegun import freeze_time

from request_time_tracker.notifiers.django_cache import DjangoCacheNotifier
from request_time_tracker.trackers.memory import InMemoryQueueTimeTracker
from tests.base import DummyWSGI, get_time_in_millis, noop


class TestDjangoCache(TestCase):
    def setUp(self):
        super().setUp()
        self.notifier = DjangoCacheNotifier(cache_name='queue-tracker-cache', cache_key_prefix='test')
        self.tracker = partial(InMemoryQueueTimeTracker, queue_time_header_name='time-header', notifier=self.notifier)
        self.wsgi = self.tracker(DummyWSGI())
        self.cache = self.notifier.get_cache()
        self.cache.set(self.notifier.get_values_cache_key(), [])

    def test_functionality(self):
        original_utcnow = datetime.utcnow()
        self.assertEqual(self.cache.get(self.notifier.get_values_cache_key(), default=None), [])
        self.assertIsNone(self.cache.get(self.notifier.get_last_value_cache_key(), default=None))

        with freeze_time(original_utcnow + timedelta(minutes=1)):
            utcnow = datetime.utcnow()
            self.wsgi({'time-header': get_time_in_millis(utcnow - timedelta(seconds=1))}, noop)

            metrics = self.cache.get(self.notifier.get_values_cache_key(), default=None)
            self.assertEqual(len(metrics), 1)
            self.assertEqual(metrics[0][0], utcnow.timestamp())
            self.assertAlmostEqual(metrics[0][1], 1, places=1)
            self.assertEqual(self.cache.get(self.notifier.get_last_value_cache_key()), metrics[0][1])

        # two metrics available
        with freeze_time(original_utcnow + timedelta(minutes=1, seconds=30)):
            utcnow = datetime.utcnow()
            self.wsgi({'time-header': get_time_in_millis(utcnow - timedelta(seconds=1.5))}, noop)

            metrics = self.cache.get(self.notifier.get_values_cache_key(), default=None)
            self.assertEqual(len(metrics), 2)
            self.assertListEqual(
                [m[0] for m in metrics],
                [(utcnow - timedelta(seconds=30)).timestamp(), utcnow.timestamp()],
            )
            self.assertAlmostEqual(metrics[1][1], 1.5, places=1)
            self.assertEqual(self.cache.get(self.notifier.get_last_value_cache_key()), metrics[1][1])

        # still two metrics available, first one is older than 2 minutes
        with freeze_time(original_utcnow + timedelta(minutes=3, seconds=1)):
            utcnow = datetime.utcnow()
            self.wsgi({'time-header': get_time_in_millis(utcnow - timedelta(seconds=3.1))}, noop)

            metrics = self.cache.get(self.notifier.get_values_cache_key(), default=None)
            self.assertEqual(len(metrics), 2)
            self.assertListEqual(
                [m[0] for m in metrics],
                [(utcnow - timedelta(minutes=1, seconds=31)).timestamp(), utcnow.timestamp()],
            )
            self.assertAlmostEqual(metrics[1][1], 3.1, places=1)
            self.assertEqual(self.cache.get(self.notifier.get_last_value_cache_key()), metrics[1][1])

    def test_no_cache_value(self):
        original_utcnow = datetime.utcnow()
        self.cache.delete(self.notifier.get_values_cache_key())
        self.assertIsNone(self.cache.get(self.notifier.get_values_cache_key(), None))

        with freeze_time(original_utcnow):
            utcnow = datetime.utcnow()
            self.wsgi({'time-header': get_time_in_millis()}, noop)

            metrics = self.cache.get(self.notifier.get_values_cache_key(), default=None)
            self.assertEqual(len(metrics), 1)
            self.assertEqual(metrics[0][0], utcnow.timestamp())
            self.assertAlmostEqual(metrics[0][1], 0, places=1)
            self.assertEqual(self.cache.get(self.notifier.get_last_value_cache_key()), metrics[0][1])

    def test_bad_cache_name(self):
        notifier = DjangoCacheNotifier(cache_name='bad_cache_name', cache_key_prefix='test')
        self.assertEqual(caches['default'], notifier.get_cache())

    def test_cache_keys(self):
        notifier = DjangoCacheNotifier(cache_name='bad_cache_name', cache_key_prefix='test')
        self.assertEqual(notifier.get_last_value_cache_key(), 'test-value')
        self.assertEqual(notifier.get_values_cache_key(), 'test-values')
