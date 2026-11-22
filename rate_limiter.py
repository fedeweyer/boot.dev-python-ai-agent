"""Rate limiter to limit calls to a maximum per second."""

import time
from collections import deque
from threading import Lock


class RateLimiter:
    """A simple sliding window rate limiter."""

    def __init__(self, max_calls: int, period: float = 1.0):
        """
        Initialize the rate limiter.

        Args:
            max_calls: Maximum number of calls allowed in the period.
            period: Time period in seconds (default 1 second).
        """
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()
        self.lock = Lock()

    def wait_if_needed(self) -> None:
        """Block until a call can be made without exceeding the rate limit."""
        with self.lock:
            now = time.time()
            # Remove timestamps older than the period
            while self.calls and self.calls[0] <= now - self.period:
                self.calls.popleft()

            if len(self.calls) >= self.max_calls:
                # Wait until the oldest call is outside the period
                oldest = self.calls[0]
                wait_time = oldest + self.period - now
                if wait_time > 0:
                    time.sleep(wait_time)
                # After sleeping, recalculate now and remove expired calls
                now = time.time()
                while self.calls and self.calls[0] <= now - self.period:
                    self.calls.popleft()

            # Record this call
            self.calls.append(now)