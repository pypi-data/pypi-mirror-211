from datetime import datetime, timedelta
from typing import Iterable, List

from request_pressure_tracker.notifiers.base import BaseNotifier
from request_pressure_tracker.trackers.base import BaseWSGIPressureTracker, PressureRecord


class InMemoryWSGIPressureTracker(BaseWSGIPressureTracker):
    def __init__(
        self, parent_application,
        target_duration_seconds: int = 60,
        send_stats_every_seconds: int = 10,
        notifiers: Iterable[BaseNotifier] = None,
    ):
        super().__init__(
            parent_application,
            target_duration_seconds=target_duration_seconds,
            send_stats_every_seconds=send_stats_every_seconds,
            notifiers=notifiers,
        )
        self.last_notified = datetime.utcnow() - timedelta(seconds=self.send_stats_every_seconds + 1)

    def check_cooldown(self) -> bool:
        return datetime.utcnow() > self.last_notified + timedelta(seconds=self.send_stats_every_seconds)

    def refresh_cooldown(self) -> None:
        self.last_notified = datetime.utcnow()

    def set_stats(self, value: List[PressureRecord]):
        self.stats = value

    def get_stats(self) -> List[PressureRecord]:
        return self.stats
