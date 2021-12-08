import sys
import time
from threading import Lock

import requests

answer_dict = {'yes': True, 'y': True, 'no': False, 'n': False}
_lock = Lock()


def get_msg_if_response_not_ok(response: requests.Response) -> str:
    try:
        response.raise_for_status()
    except Exception as e:
        return str(e)


def get_answer_yes_or_no() -> bool:
    try:
        answer = answer_dict[input().lower()]
    except KeyError:
        print('Abort.')
        sys.exit()

    return answer


def wrapper_requests_get(url, timeout):
    _lock.acquire()
    response = requests.get(url)
    time.sleep(timeout)
    _lock.release()
    return response
