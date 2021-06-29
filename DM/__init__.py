from DM.profile_fetcher import profile_fetcher
from DM.DestinyManager import get_characters, character_milestone_prog

from p_var import CLASS_REF, ENV

from typing import Optional, Union, List
import json
import os

from pprint import pprint


class ProfileManager:
    def __init__(self):
        self._ind = {}
        self.laod_data()

    def search(self, qq: int) -> Optional[profile_fetcher]:
        if qq in self._ind.keys():
            return self._ind[qq]
        else:
            return None

    @staticmethod
    def load():
        ENV['cmd'].extend([
            ("绑定", ProfileManager.insert_wrapper),
            ("周常", ProfileManager.milestone_wrapper)
        ])

    @staticmethod
    def insert_wrapper(rd, *args):
        qq = int(rd['sender']['id'])
        res = []
        if len(args) == 1:
            res.append({"type": "Plain", "text": "参数数量错误"})
        else:
            rv = ENV['pm'].insert(qq, args[1])
            if rv != 0:
                res.append({"type": "Plain", "text": "BungieID参数错误"})
            else:
                res.append({"type": "Plain", "text": "绑定成功"})
        return res, True

    def insert(self, qq: int, bungieId: str) -> int:
        pf = profile_fetcher(bungieId)
        rv = pf.get_membership_type()
        if rv != 0:
            return -1
        else:
            self._ind[qq] = pf
            self.save_data()
            return 0

    @staticmethod
    def milestone_wrapper(rd, *args):
        qq = int(rd['sender']['id'])
        rv = ENV['pm'].milestone_progress(qq)

        return rv, True

    def milestone_progress(self, qq: int, ind: int = 0) -> Union[int, List]:
        res = self.search(qq)
        if not res:
            return [{"type": "Plain", "text": "请先绑定BungieID"}]
        print(res.membershipData)
        m_data = res.membershipData[ind]
        print(m_data)
        char_prog, char_data = get_characters(membershipType=m_data[0], destinyMembershipId=m_data[1])
        res = {}
        print(char_prog.keys())
        for k, v in char_prog.items():
            pprint(v)
            res[(k, CLASS_REF[char_data[k]['classType']])] = character_milestone_prog(v)
            # 1 Hunter 2 Warlock 3 Tital
        print(res)
        tl = [i for i in res.keys()]
        sd = ""
        for i in tl:
            sd += i[1] + " "
        sd = f"({sd})\n"
        mv = max(tl, key=lambda x: len(res[x]))
        for vk in res[mv].keys():
            ts = " "
            for i in tl:
                if vk not in res[i].keys():
                    ts += "U "
                elif res[i][vk]['status'] == "Finished":
                    ts += "● "
                else:
                    ts += "X "
            ts = f"({ts}): {vk}\n"
            sd += ts
        return [{"type": "Plain", "text": sd}]

    def save_data(self):
        tmp = {}
        for k, v in self._ind.items():
            tmp[k] = v.save_data()
        with open("./data/user_data.json", 'w') as f:
            json.dump(tmp, f)

    def laod_data(self):
        if os.path.isfile("./data/user_data.json"):
            with open("./data/user_data.json", 'r') as f:
                res = json.load(f)
                for k, v in res.items():
                    pf = profile_fetcher()
                    pf.load_data(v)
                    self._ind[int(k)] = pf


ENV['pm'] = ProfileManager()
ProfileManager.load()
print("DestinyManager loaded")
