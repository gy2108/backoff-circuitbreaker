import time
import requests


def backoff_retry(retries=3, backoff_in_seconds=1):
    """
    Decorator with back off retry algo
    :param retries: number of attempt to try(default is 3)
    :param backoff_in_seconds: multiplier for delay  in each try
    """
    def rwb(f):
        def wrapper(*args, **kwargs):
            tries = 0
            while True:
                try:
                    return f(*args, **kwargs)
                except:
                    if tries == retries:
                        return f(*args, **kwargs)
                    else:
                        sleep = (backoff_in_seconds * 2 ** tries)
                        time.sleep(sleep)
                        tries += 1
        return wrapper
    return rwb


@backoff_retry(retries=5)
def get_resource(url, port):
    response = requests.get("http://{}:{}/".format(url, port))
    return response.text