
from queue import LifoQueue
import threading
import time
from typing import Any

BUCKET_SIZE = 30
INTERVAL = 1.0  # float seconds


class RateLimitException(Exception):
    '''Custome exception Inhariting from Exception class'''
    def __init__(self, message: str) -> None:
        '''Raise a a exception with given message'''
        super(RateLimitException, self).__init__(message)


class TokenBucket:
    def __init__(self, max_api_call,raise_on_limit=True):
        '''Create a dequeue object with maximum size.'''
        # Initializing a Bucket-stack
        self.api_call = min(max_api_call, BUCKET_SIZE)
        self.stack = LifoQueue(maxsize=self.api_call)
        self.raise_on_limit=raise_on_limit
        # Add thread safety.
        self.lock = threading.RLock()
        # Initiate Refile Mechanism
        self.is_bucket_empty = True
        self.refile_bucket()

    def grant_token(self):
        '''Give a token from bucket and raise if empty'''
        with self.lock:
            if self.stack.empty():
                # fill bucket
                self.is_bucket_empty = True
                self.refile_bucket()
                # raise limit exeception
                if self.raise_on_limit:
                    raise RateLimitException("Reached Max Api calls for time")
                return
            self.stack.get(1)

    def refile_bucket(self):
        '''Refill bucket every second, if bucket is missing token'''
        while self.is_bucket_empty:
            time.sleep(INTERVAL)
            if not self.stack.full():
                with self.lock:
                    # for _ in range(max(2,self.api_call-self.stack.qsize())):
                    for _ in range(self.api_call-self.stack.qsize()):
                        self.stack.put(1)
                    self.is_bucket_empty = False
