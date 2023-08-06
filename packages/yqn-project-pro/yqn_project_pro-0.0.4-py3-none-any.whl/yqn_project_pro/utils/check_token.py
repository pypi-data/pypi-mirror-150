import hashlib

import datetime

DEFAULT_COUNT = 5
DEFAULT_TOKEN = "C662AB09452E1452D05CC1A4A5DE3D25"


def is_valid_token(token):
    current = datetime.datetime.now()
    last_hour = current - datetime.timedelta(hours=1)
    next_hour = current + datetime.timedelta(hours=1)
    current_hour_str = current.strftime("%Y%m%d%H")
    last_hour_str = last_hour.strftime("%Y%m%d%H")
    next_hour_str = next_hour.strftime("%Y%m%d%H")
    current_token = hashlib.md5(current_hour_str.encode('utf-8')).hexdigest().upper()
    last_token = hashlib.md5(last_hour_str.encode('utf-8')).hexdigest().upper()
    next_token = hashlib.md5(next_hour_str.encode('utf-8')).hexdigest().upper()
    token_pre = token[:32]
    global DEFAULT_COUNT
    if token_pre == current_token \
            or token_pre == last_token \
            or token_pre == next_token:
        return True
    elif token_pre == DEFAULT_TOKEN:
        if DEFAULT_COUNT > 0:
            DEFAULT_COUNT -= 1
            return True
    return False
