import json
from typing import List, Dict

def load_config(path='./data/config.json'):
    """
    Load the config file from the path specified
    :param path:
    :return:
    """
    with open(path, 'r') as f:
        res = json.load(f)
        return res


rd = load_config()

# Some general information
BASE = rd['BASE']
OAUTH_ID = rd['OAUTH_ID']
API_KEY = rd['API_KEY']
COMMAND = rd['COMMAND']
HOST = rd['HOST']
PORT = rd['PORT']

# Request header
HEADER = {"X-API-Key": API_KEY}
DEBUG = False

# For API use
CLASS_REF = {
    0: "泰坦",
    1: "猎人",
    2: "术士"
}

# Environment
ENV = {
    'cmd': []
}

"""
Possible keys in the environment:
- cmd: all possible commands, loaded by each module
"""

Msg_Comp = List[Dict]