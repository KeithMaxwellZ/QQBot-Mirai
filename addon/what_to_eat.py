from p_var import ENV, Msg_Comp
from typing import Dict, List, Tuple

import random
import os


class WhatToEat:
    def __init__(self):
        """
        Load the files from directory
        DO NOT MODIFY THE FILES WHILE THE BOT IS RUNNING
        """
        self.files = os.listdir("./addon/what_to_eat/foodimg/")
        self.queue = []

    @staticmethod
    def load():
        """
        Load the command into the environment
        :return:
        """
        ENV['cmd'].extend([("今天吃什么", WhatToEat.decide_wrapper)])

    @staticmethod
    def decide_wrapper(rd: Dict, args: Tuple) -> Tuple[Msg_Comp, bool]:
        """
        Wrapper class for decide function
        arguments are not needed but just need to be there
        :param rd:
        :param args:
        :return:
        """
        res = ENV['wte'].decide()
        return res, True

    def decide(self) -> Msg_Comp:
        """
        Function for randomly choose an image and return its path and name
        :return: return a message component
        """
        # Using queue to reduce the amount of duplication
        if not self.queue:
            self.queue = [i for i in range(0, len(self.files))]
            random.shuffle(self.queue)
            self.queue = self.queue[0:10]

        # Get one element from the queue
        r = self.queue.pop()
        name = self.files[r].split('.')[0]

        # Form message components
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