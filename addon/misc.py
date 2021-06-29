from p_var import ENV


class Misc:
    def __init__(self):
        cmds = [
            ("矩阵挑食", Misc.ts),
            ("蛇打结", Misc.snake)
        ]
        ENV['cmd'].extend(cmds)
        print("Misc loaded")

    @staticmethod
    def ts(_, __, *args):
        return [{"type": "Plain", "text": "不可以挑食！"}], False

    @staticmethod
    def snake(_, __, *args):
        img = {
            "type": "Image",
            "imageId": None,
            "url": None,
            "path": f"misc/snake.jpg",
            "base64": None
        }

        return [img], False


ms = Misc()
