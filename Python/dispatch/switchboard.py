import asyncio
from typing import Any, Dict, Optional, Tuple

from attr import attrib, attrs


@attrs(slots=True)
class SwitchBoard:
    active_workers: Dict[Any, asyncio.Lock] = attrib(default={})
    least_important: Tuple[Optional[float], Optional[Any]] = attrib(default=(None, None))

    @property
    def num_active_workers(self) -> int:
        return len([k for k, v in self.active_workers.items() if v.locked()])

    def unlock_worker(self, worker: Any) -> None:
        # has to exist
        if worker not in self.active_workers:
            raise ValueError("hey, I dun no nuttin' 'bout dat")

        # cannot already be released
        if not self.active_workers[worker].locked():
            raise ValueError("hey, I'm (already) working here!")

        # check if now least important worker
        if self.least_important[0] is None or worker.priority < self.least_important[0]:
            # we use LT instead of LTE here so that on tie, newest worker isn't constantly picked to be paused
            self.least_important = (worker.priority, worker)

        # let worker work!
        self.active_workers[worker].release()

    def retire_worker(self, worker: Any) -> None:
        try:
            self.active_workers[worker].release()
        except RuntimeError:
            pass
        del self.active_workers[worker]

        if self.least_important[1] == worker:
            self.set_least_important_active_worker()

    def set_least_important_active_worker(self) -> None:
        # TODO may call for min heap a la PriorityQueue
        self.least_important = (None, None)
        for worker, lock in self.active_workers.items():
            if not lock.locked():  # not active
                continue
            if self.least_important[0] is None or worker.priority < self.least_important[0]:
                self.least_important = (worker.priority, worker)
