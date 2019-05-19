from datetime import datetime


def get_timestamp():
    now = datetime.now()
    return now.strftime("%Y_%m_%d_%h_%M_%S_%f")
