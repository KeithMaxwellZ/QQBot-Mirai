import pickle
import os


class DFA:
    class Transitions:
        def __init__(self, fr, to):
            self.fr = fr
            self.to = to

        def __eq__(self, other):
            if type(other) is DFA.Transitions:
                return self.fr == other.fr and self.to == other.to

        def __hash__(self):
            if self.fr:
                return hash(f"{self.fr}{self.to}")
            return hash(self.to)

        def __str__(self):
            return f"from {self.fr} to {self.to}"

    def __init__(self, data_path: str = "./data/conv.pickle"):
        self.states = set()
        self.transitions = set()
        self.fs = dict()
        self.data_path = data_path

    def _insert_transition(self, fr, to):
        self.states.add(fr)
        self.states.add(to)
        self.transitions.add(DFA.Transitions(fr, to))

    def insert(self, word):
        if len(word) == 0:
            return -1
        else:
            self.transitions.add(DFA.Transitions(None, word[0]))
            for i in range(0, len(word) - 1):
                self.transitions.add((DFA.Transitions(word[i], word[i + 1])))
            if word[-1] in self.fs:
                self.fs[word[-1]].append(word)
            else:
                self.fs[word[-1]] = [word]

    def match(self, word):
        curr = None
        i = 0
        cache = ""
        res_l = []
        while i < len(word):
            if DFA.Transitions(curr, word[i]) in self.transitions:
                curr = word[i]
                cache += word[i]
            else:
                curr = None
                cache = ""
            if curr in self.fs:
                for x in self.fs[curr]:
                    v = cache.rfind(x)
                    if v != -1 and v + len(x) == len(cache):
                        res_l.append(x)
            i += 1

        return res_l

    def debug(self):
        for i in self.transitions:
            print(f"from {i.fr} to {i.to}")

    def save(self):
        with open(self.data_path, 'wb') as f:
            pickle.dump((self.states, self.transitions, self.fs), f)

    def load(self):
        if os.path.isfile(self.data_path):
            with open(self.data_path, 'rb') as f:
                lst = pickle.load(f)
                self.states = lst[0]
                self.transitions = lst[1]
                self.fs = lst[2]


if __name__ == '__main__':
    dfa = DFA()
    # dfa.debug()
    # dfa.insert("东北")
    # dfa.insert("我")
    # dfa.insert("你")
    # dfa.insert("在东北")

    print(dfa.match("我在东北玩泥巴"))
    print(dfa.match("你是谁"))
    print(dfa.match("他和我"))
    print(dfa.match("是谁在东北"))
    print(dfa.match("random"))

    dfa.save()