from util.DFA import DFA
from p_var import ENV
import random
import json
import os
from pprint import pprint

ACTIVATE = True


class ConversationManager:
    def __init__(self):
        self.dfa = DFA()
        self.ref = {}
        self.load_data()

    @staticmethod
    def load():
        cmds = [
            ("添加对话", ConversationManager.insert_wrapper),
            ("删除对话", ConversationManager.delete_wrapper),
            ("#对话调试", ConversationManager.debug_wrapper),
        ]
        ENV['cmd'].extend(cmds)
        print("Misc loaded")

    @staticmethod
    def insert_wrapper(rd, args):
        if len(args) == 3:
            ENV['cm'].insert(rd['sender']['group']['id'], args[1], args[2])
            s = f"添加成功\n关键词: {args[1]}\n回应: {args[2]}"
            return [{'type': 'Plain', 'text': s}], True
        elif len(args) == 4:
            ENV['cm'].insert(int(args[3]), args[1], args[2])
            s = f"添加成功\n关键词: {args[1]}\n回应: {args[2]}\n群：{args[3]}"
            return [{'type': 'Plain', 'text': s}], True
        else:
            return [{'type': 'Plain', 'text': "参数数量错误"}], True

    def insert(self, group, word, resp):
        if group not in self.ref:
            self.ref[group] = dict()
        if word in self.ref[group]:
            self.ref[group][word].append(resp)
        else:
            self.ref[group][word] = [resp]
            self.dfa.insert(word)
        self.save_data()

    @staticmethod
    def delete_wrapper(rd, args):
        if len(args) == 2:
            ENV['cm'].delete(rd['sender']['group']['id'], args[1])
            s = f"移除成功"
            return [{'type': 'Plain', 'text': s}], True
        elif len(args) == 3:
            ENV['cm'].delete(int(args[2]), args[1])
            s = f"移除成功2"
            return [{'type': 'Plain', 'text': s}], True
        else:
            return [{'type': 'Plain', 'text': "参数数量错误"}], True

    def delete(self, group, word):
        print(group, word)
        if group in self.ref and word in self.ref[group]:
            self.ref[group].pop(word)
        self.save_data()

    def search(self, group, sentence):
        if group in self.ref:
            res_l = self.dfa.match(sentence)
            # TODO: Test it
            resp_lst = []
            if res_l:
                for w in res_l:
                    if w in self.ref[group]:
                        resp_lst.extend(self.ref[group][w])

            p = random.randint(0, 100)
            if p < 30:
                val = random.randint(0, len(resp_lst) - 1)
                return [{'type': 'Plain', 'text': resp_lst[-1]}]

        return []

    def save_data(self):
        with open('./plugin/conversation/data.json', 'w') as f:
            json.dump(self.ref, f)

    def load_data(self):
        if os.path.isfile('./plugin/conversation/data.json'):
            with open('./plugin/conversation/data.json', 'r') as f:
                tl = json.load(f)
                for i in tl:
                    self.ref[int(i)] = tl[i]
                for i in self.ref.keys():
                    for w in self.ref[i].keys():
                        self.dfa.insert(w)

    @staticmethod
    def debug_wrapper(rd, args):
        return ENV['cm'].debug()

    def debug(self):
        pprint(self.ref)
        return [], False


ENV['cm'] = ConversationManager()
if ACTIVATE:
    ENV['cm'].load()
    ENV['ACTV_cm'] = True
