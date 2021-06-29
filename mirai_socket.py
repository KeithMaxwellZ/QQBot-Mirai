from p_var import DEBUG
from util.message_parser import ParserManager

import websocket
import json
import requests
import traceback

from pprint import pprint


def on_message(ws: websocket.WebSocketApp, msg):
    data = json.loads(msg)
    if DEBUG:
        print("===== Message =====")
        print(msg)
        pprint(data)
    if data["type"] == "GroupMessage" and len(data["messageChain"]) == 2:
        for i in data["messageChain"]:
            if i["type"] == "Plain":
                if DEBUG:
                    print(i)
                    print(i["text"])
                try:
                    chain = pm.parse(i["text"], data)
                    if chain:
                        session = rj1['session']
                        target = data["sender"]["group"]["id"]
                        print(session)
                        print(chain)
                        print(target)
                        send_group_message(session, chain, target)
                except Exception as e:
                    traceback.print_exc()


def on_error(ws: websocket.WebSocketApp, *args):
    if DEBUG:
        print("===== ERROR =====")
        print(args)


def on_close(ws: websocket.WebSocketApp, *args):
    if DEBUG:
        print("===== Close =====")
        print(args)


def on_open(ws: websocket.WebSocketApp):
    if DEBUG:
        print("===== Open =====")
    about_payload = {
        "syncId": 1,
        "command": "about",
        "subCommand": None,
        "content": {}
    }
    req = json.dumps(about_payload)
    print(req)
    r = ws.send(req)
    print(r)


res = requests.post("http://localhost:8081/auth", data=json.dumps({"authKey": "kmw001115"}))
rj1 = res.json()
print(rj1)

res = requests.post("http://localhost:8081/verify",
                    data=json.dumps({"sessionKey": rj1['session'], "qq": 2797339190}))
rj2 = res.json()
print(rj2)

if DEBUG:
    websocket.enableTrace(True)

head = {
    "sessionKey": rj1['session'],
}

wst = websocket.WebSocketApp(f"ws://localhost:8081/all?sessionKey={rj1['session']}",
                             on_message=on_message,
                             on_error=on_error,
                             on_close=on_close)
pm = ParserManager()


def run():
    print("Starting server")
    wst.run_forever()
