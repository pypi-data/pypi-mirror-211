from datetime import datetime, timedelta
from functools import partial
from unittest import TestCase

from freezegun import freeze_time

from request_pressure_tracker.trackers.memory import InMemoryWSGIPressureTracker
from tests.base import DummyNotifier, DummyWSGI


class TestMemoryTracker(TestCase):
    def test_pressure_count(self):
        tracker = partial(
            InMemoryWSGIPressureTracker, target_duration_seconds=5 * 60, notifiers=[DummyNotifier]
        )(DummyWSGI())

        with freeze_time(datetime(1970, 10, 1, 0, 5, 10)):
            tracker.count_request(datetime(1970, 10, 9, 0, 0, 0), timedelta(seconds=60))
            tracker.count_request(datetime(1970, 10, 10, 0, 0, 0), timedelta(seconds=60))
            tracker.count_request(datetime(1970, 10, 10, 0, 3, 0), timedelta(seconds=25))
            tracker.count_request(datetime(1970, 10, 10, 0, 3, 26), timedelta(seconds=40))
            tracker.count_request(datetime(1970, 10, 10, 0, 5, 1), timedelta(seconds=8))

        self.assertEqual(len(tracker.get_stats()), 5)

        with freeze_time(datetime(1970, 10, 10, 0, 5, 30)):
            tracker.count_request(datetime(1970, 10, 10, 0, 5, 10), timedelta(seconds=9))
            self.assertEqual(len(tracker.get_stats()), 5)
            self.assertEqual(
                tracker.get_pressure(),
                timedelta(seconds=((60 - 30) + 25 + 40 + 8 + 9)) / timedelta(minutes=5)
            )
