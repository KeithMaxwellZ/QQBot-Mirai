import json


def load_config(path='./data/config.json'):
    with open(path, 'r') as f:
        res = json.load(f)
        return res['BASE'], res['OAUTH_ID'], res['API_KEY'], res['COMMAND'], res['HOST'], res['PORT']


BASE, OAUTH_ID, API_KEY, COMMAND, HOST, PORT = load_config()
HEADER = {"X-API-Key": API_KEY}
DEBUG = False

CLASS_REF = {
    0: "泰坦",
    1: "猎人",
    2: "术士"
}


ENV = {
    'cmd': []
}

"""
Possible keys in the environment:
- cmd: all possible commands, loaded by each module
"""