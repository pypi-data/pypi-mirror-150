import time
from datetime import datetime

from .base import ThrottleBase


class Throttle(ThrottleBase):

    def call(self):
        sleep_time = self._call()
        time.sleep(sleep_time)
        self._last_call_time = datetime.now()
