from p_var import ENV

from util.util import text_payload_gen, image_payload_gen


class Misc:
    """
    Some random stuff, will be replaced by conversation manager later
    """

    def __init__(self):
        cmds = [
            ("矩阵挑食", Misc.ts),
            ("蛇打结", Misc.snake),
            ("ip", Misc.ip)
        ]
        ENV['cmd'].extend(cmds)
        print("Misc loaded")

    @staticmethod
    def ts(*_):
        return [text_payload_gen("不可以挑食！")], False

    @staticmethod
    def snake(*_):
        return [image_payload_gen(f"misc/snake.jpg")], False

    @staticmethod
    def ip(_, __, *args):
        return [{"type": "Plain", "text": "101.34.13.221:25567"}], True


ms = Misc()
