# Program to store last 10 minutes of data from API to Redis
#
# Data for every person is saved as Redis list under key personData{id}
# Every list entry is **JSON serialized** server response
#
# Before running this script there needs to be Redis instance running.
# Simplest way to achieve this is to run Docker image: docker run --rm -p 6379:6379 --name redis -it redis
#
# To add redis-py library to Anaconda run: conda install -c anaconda redis-py

import redis
import requests
import json
from datetime import datetime, timedelta
import time
import sys
import os

REDIS_HOST = os.getenv('REDIS_HOST') or 'localhost'
store = redis.Redis(REDIS_HOST)

base_url = 'http://tesla.iem.pw.edu.pl:9080/v2/monitor'
data_expiration_time = timedelta(minutes=10)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def add_all_data() -> None:
    """Fetch and save to redis data about every person
    """

    for i in range(1, 7):
        add_singe_data(i)


def add_singe_data(id: int) -> None:
    """Fetch and save to redis current data about one person
    If API doesn't respond no data is saved

    Arguments:
        id {int} -- Endpoint person id from 1 to 6
    """

    url = f'{base_url}/{id}'

    r = None
    try:
        r = requests.get(url, timeout=5)
    except requests.ConnectionError:
        print(
            f'{bcolors.FAIL}Unable to fetch data from the server{bcolors.ENDC}', flush=True)
        print('Make sure that VPN connection is enabled\n', flush=True)
        return

    if r.status_code != 200:  # Failed to get data
        return

    data = r.json()
    data["timestamp"] = datetime.timestamp(datetime.now())  # Add current time

    key = f'personData{id}'
    store.lpush(key, json.dumps(data, separators=(',', ':')))


def clean_all_data() -> None:
    """Remove oldest records in every list if it's time stamp is pass given time"""

    for i in range(1, 7):
        clean_singe_data(i)


def clean_singe_data(id: int) -> None:
    """Remove oldest records in list with given id if it's time stamp is pass given time"""
    key = f'personData{id}'

    # It could be inefficient. Maybe we should pop and push it back if it's ok
    oldest_data = store.lrange(key, -1, -1)[0]
    oldest_data = json.loads(oldest_data)

    if datetime.fromtimestamp(oldest_data["timestamp"]) < datetime.now() - data_expiration_time:
        store.rpop(key)


def initial_cleanup() -> None:
    """Delete all data from previous runs"""
    keys = [f'personData{id}' for id in range(1, 7)]
    store.delete(*keys)


if __name__ == '__main__':
    print('Starting to cache API data for rough times', flush=True)
    initial_cleanup()

    try:
        while True:
            add_all_data()
            clean_all_data()
            time.sleep(0.8)  # Try to have one data point every second
    except KeyboardInterrupt:
        print('\nSavin API data stopped, bye bye', flush=True)
