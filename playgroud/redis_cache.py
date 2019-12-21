# Program to store last 10 minutes of data from API to Redis
# Currently data is **never deleted**
#
# Before running this script there needs to be Redis instance running.
# Simplest way to achieve this is to run Docker image: docker run --rm -p 6379:6379 --name redis -it redis
#
# To add redis-py library to Anaconda run: conda install -c anaconda redis-py

# Data of each person will be added to separate list

import redis
import requests
import json
from datetime import datetime
import time
import sys

base_url = 'http://tesla.iem.pw.edu.pl:9080/v2/monitor'
store = redis.Redis()


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
        print('Unable to fetch data from the server')
        print('Make sure that VPN connection is enabled\n')
        return

    if r.status_code != 200:  # Failed to get data
        return

    data = r.json()
    data["timestamp"] = datetime.timestamp(datetime.now())  # Add current time

    key = f'personData{id}'
    store.lpush(key, json.dumps(data, separators=(',', ':')))


if __name__ == '__main__':
    while True:
        add_all_data()
        time.sleep(0.8)  # Try to have one data point every second
