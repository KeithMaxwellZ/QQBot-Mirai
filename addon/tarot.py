import json
import random

from p_var import DEBUG, ENV
from pprint import pprint
from datetime import datetime

from typing import Dict, Tuple, List


def load():
    # load the preprocessed text data
    with open("./addon/tarot/tarot_data.txt", 'r') as f:
        res = json.load(f)
        return res


ACTIVATE = True


class TarotManager:
    def __init__(self):
        self.cache = []
        self.pv1 = -1
        self.today = datetime.now()
        self.load_cache()

        self.rf = {
            "女装": {
                "pos": [
                    "嗯",
                    "嗯？",
                ],
                "neg": [
                    "嗯",
                    "嗯？",
                ]
            },
            "PVP": {
                "pos": [
                    "随便打打就是一个第七砥柱",
                    "一带五照样稳赢",
                    "乱杀",
                ],
                "neg": [
                    "nmd，又是连体",
                    "对面又是轮椅飞行",
                    "蓝装萌新警告"
                ]
            },
            "抽卡": {
                "pos": [
                    "单抽出货",
                    "双黄蛋",
                ],
                "neg": [
                    "歪了",
                    "蓝天白云",
                    "紫气东来"
                ]
            },
            "智谋": {
                "pos": [
                    "对面掉线了两个！",
                    "我方入侵把对面杀穿了！",
                    "好耶，重弹药捡满了",
                ],
                "neg": [
                    "nmd，怎么这边也是是连体",
                    "呜呜，对面入侵好猛"
                    "队友15块警告",
                    "蓝装萌新警告"
                ]
            },
            "宗师日暮": {
                "pos": [
                    "出金了，30恢复30智慧",
                    "今日适宜进货",
                ],
                "neg": [
                    "上纬碎片x1",
                    "飞龙跳脸了！",
                ]
            },
            "raid": {
                "pos": [
                    "这把一定出金",
                    "好，是GR",
                ],
                "neg": [
                    "出金了，小白鞋",
                    "又双叒被演了",
                    "速通变宿通",
                ]
            },
            "音游": {
                "pos": [
                    "All Perfect",
                    "无情的推分机器",
                ],
                "neg": [
                    "你有一个好",
                    "你有一个小姐",
                    "交互变双押，准度___",
                ]
            },
            "外出": {
                "pos": [
                    "阳光明媚，适宜外出",
                    "说不定会有什么特别的遭遇",
                ],
                "neg": [
                    "艹，忘带伞了",
                    "艹，忘带交通卡了",
                    "艹，忘带钱包了",
                ]
            },
            "摸鱼": {
                "pos": [
                    "摸鱼使我快乐",
                    "加班是不可能的，到点一定准时跑路",
                ],
                "neg": [
                    "抓到了，就是你在摸鱼",
                ]
            },
            "逛街": {
                "pos": [
                    "说不定会碰上什么好事"
                ],
                "neg": [
                    "冲动消费警告",
                ]
            },
            "mc": {
                "pos": [
                    "挖到钻石了",
                    "灵感如泉涌",
                ],
                "neg": [
                    "房子被小黑拆了！",
                    "屋顶又刷怪了！",
                ]
            },
            "复读": {
                "pos": [
                    "人类的本质是复读机",
                ],
                "neg": [
                    "管理：让我康康是谁在复读",
                ]
            },
        } # Possible outcomes

    @staticmethod
    def load():
        """
        load commands in to the environment
        :return:
        """
        ENV['cmd'].extend([
            ("抽签", TarotManager.draw_wrapper),
            ("#检查缓存", TarotManager.show_cache_wrapper)
        ])

    @staticmethod
    def draw_wrapper(rd: Dict, args: Tuple) -> Tuple[List[Dict], bool]:
        """
        Wrapper class for draw function
        :param rd: The original dict from the request
        :param args: It's not used but is needed
        :return: The result of the draw function,
                 will mentioned the user who invoked this command
        """
        qq = int(rd['sender']['id'])
        res = ENV['tm'].draw(qq)
        return res, True

    @staticmethod
    def show_cache_wrapper(*args):
        """
        For debug only, will print the result to the console
        :param args:
        :return:
        """
        ENV['tm'].show_cache()
        return [], False

    def draw(self, qq: int) -> List[Dict]:
        """
        Function for drawing a tarot card
        :param qq: check if the user has drawn the card already or not
        :return: The tarot card or error message
        """

        if DEBUG:
            # DEBUG mode will clear the cache every time the command is invoked
            self.cache.clear()

        # Check if the day has changed and reset the cache if necessary
        curr = datetime.now()
        if not (curr.day == self.today.day and curr.month == self.today.month and curr.year == self.today.year):
            self.cache.clear()
            self.today = curr

        # Check of the caller has already drawn the tarot
        if qq in self.cache:
            return [{'type': 'Plain', 'text': "今天已经抽过了，请明天再来"}]
        else:
            self.cache.append(qq)
            self.save_cache()

        ref = {0: "逆位", 1: "正位"}

        # Decide card id and direction
        v1 = random.randint(0, 21)
        while v1 == self.pv1:
            v1 = random.randint(0, 21)
        self.pv1 = v1
        v2 = random.randint(0, 1)

        rd = r[f"{v1}"].copy()
        rd: dict
        if v2 == 0:
            rd.pop("正位")
        else:
            rd.pop("逆位")

        # Concatenate the string
        sd = f"\n\n{rd['牌名']}\n" \
             f"核心：{rd['关键语']}\n" \
             f"事件：{rd['暗示']}\n" \
             f"\n" \
             f"[{ref[v2]}] \n\n" \
             f"[忌宜]"

        for k, v in rd[ref[v2]].items():
            sd += f"{k}: {v}\n"

        # Generate to pros and cons (?
        # By using shuffle to avoid duplication
        cand = [i for i in self.rf.keys()]
        random.shuffle(cand)
        p = cand.pop()
        n = cand.pop()
        pv = random.randint(0, len(self.rf[p]['pos']) - 1)
        nv = random.randint(0, len(self.rf[n]['neg']) - 1)

        # Concatenate the string
        s = f"[忌宜]\n" \
            f"适宜 {p}: {self.rf[p]['pos'][pv]}\n" \
            f"忌讳 {n}: {self.rf[n]['neg'][nv]}\n"

        sd += '\n' + s

        # Form payloads
        img = {
            "type": "Image",
            "imageId": None,
            "url": None,
            "path": f"img/838_{str(v1).zfill(2)}.jpg",
            "base64": None
        }

        rs = {'type': 'Plain', 'text': sd}
        return [img, rs]

    def show_cache(self):
        """
        For debug only
        :return: no return
        """
        pprint(self.cache)

    def save_cache(self):
        """
        Save the list of users who has drawn the tarot
        :return: no return
        """
        with open("./addon/tarot/cache", 'w') as f:
            rd = {
                "cache": self.cache,
                "date": self.today.strftime("%y-%m-%d")
            }
            json.dump(rd, f)

    def load_cache(self):
        """
        Load the list of users who has drawn the tarot
        :return: no return
        """
        with open("./addon/tarot/cache", 'r') as f:
            rd = json.load(f)
            self.cache = rd['cache']
            self.today = datetime.strptime(rd['date'], "%y-%m-%d")


# Initializations
r = load()
ENV['tm'] = TarotManager()
if ACTIVATE:
    ENV['tm'].load()
print("Tarot module imported")