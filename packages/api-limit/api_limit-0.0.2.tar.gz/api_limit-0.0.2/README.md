# Api_Limit

## About

It's Simple Middeleware implemented with tocken bucket algorithm to manage the number of api per seconds.

## Usage
```
import time
from api_limit import api_limit
import requests

@api_limit(max_api_call=2)
def call_api(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))
    return response
```

We can also specify wheter overflow of call should return the response or simply avoide the call without acknowledgement.