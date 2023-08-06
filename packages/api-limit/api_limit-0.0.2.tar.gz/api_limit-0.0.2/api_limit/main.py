
from typing import Any
import json
from functools import wraps
from .algorithm import TokenBucket, RateLimitException
from http import HTTPStatus

# api_limit = TokenBucket


class ApiRateLimiter(object):
    def __init__(self, max_api_call, raise_on_limit=True, algorithm=TokenBucket) -> None:
        '''
        '''
        self.algorithm = algorithm(max_api_call,raise_on_limit)

    def __call__(self, func) -> Any:
        '''Wrapper function'''
        @wraps(func)
        def wrapper(*args, **kargs):
            '''Gives a token to make an api call'''
            try:
                self.algorithm.grant_token()
            except RateLimitException:
                return json.dumps({
                    "Response": "Limit Exceeded",
                    "status_code": HTTPStatus.TOO_MANY_REQUESTS
                })
            return func(*args, **kargs)
        return wrapper


__all__ = ["ApiRateLimiter", "TokenBucket"]
