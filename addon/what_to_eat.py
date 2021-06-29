from p_var import ENV

import random
import os


class WhatToEat:
    def __init__(self):
        self.files = os.listdir("./addon/what_to_eat/foodimg/")
        self.queue = []


    @staticmethod
    def load():
        ENV['cmd'].extend([("今天吃什么", WhatToEat.decide_wrapper)])

    @staticmethod
    def decide_wrapper(rd, args):
        res = ENV['wte'].decide()
        return res, True

    def decide(self):
        if not self.queue:
            self.queue = [i for i in range(0, len(self.files))]
            random.shuffle(self.queue)
            self.queue = self.queue[0:10]
        r = self.queue.pop()
        name = self.files[r].split('.')[0]
        img = {
            "type": "Image",
            "imageId": None,
            "url": None,
            "path": f"foodimg/{name}.jpg",
            "base64": None
        }
        text = {'type': 'Plain', 'text': '\n' + name}
        return [img, text]


ACTIVATE = True
ENV['wte'] = WhatToEat()
if ACTIVATE:
    ENV['wte'].load()
print("what_to_eat module imported")