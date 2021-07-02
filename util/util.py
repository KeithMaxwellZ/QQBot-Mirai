from p_var import HOST, PORT

import requests
import json
from typing import Dict

def send_group_message(sessionkey: str, content: list, target: int):
    pl = {
        "sessionKey": sessionkey,
        "target": target,
        "messageChain": content
    }

    res = requests.post(f"http://{HOST}:{PORT}/sendGroupMessage", data=json.dumps(pl))
    rj = res.json()
    if rj['code'] != 0:
        print(rj)


def send_friend_message(sessionkey: str, content: list, target: int):
    pl = {
        "sessionKey": sessionkey,
        "target": target,
        "messageChain": content
    }

    res = requests.post(f"http://{HOST}:{PORT}/sendFriendMessage", data=json.dumps(pl))
    rj = res.json()
    if rj['code'] != 0:
        print(rj)


def text_payload_gen(msg: str, ending="") -> Dict:
    return {'type': 'Plain', 'text': f'{msg}{ending}'}


def image_payload_gen(path: str) -> Dict:
    return {
            "type": "Image",
            "imageId": None,
            "url": None,
            "path": f"{path}",
            "base64": None
        }