from p_var import COMMAND, ENV


def test_command():
    def func(_, __, *args):
        return [{"type": "Plain", "text": "SUCCESS"}], True

    return [("TEST", func)]


class ParserManager:
    def __init__(self):
        ENV['cmd'].extend(test_command())

    def parse(self, msg: str, rd: dict):
        res = []
        if msg[0] == COMMAND:
            print(msg)
            c = msg.split(' ')
            i = 0
            while i < len(c):
                if c[i] == " ":
                    c.remove(c[i])
                else:
                    i += 1
            raw = c[0][1:]
            qq = int(rd['sender']['id'])
            res = []

            matched = False
            for i in ENV['cmd']:
                if raw == i[0]:
                    matched = True
                    tr, at = i[1](rd, tuple(c))
                    if tr:
                        if at:
                            res.extend([{'display': '', 'target': qq, 'type': 'At'},
                                        {"type": "Plain", "text": "\n"}])
                        res.extend(tr)
                    break

            if not matched:
                res.extend([{'display': '', 'target': qq, 'type': 'At'},
                            {"type": "Plain", "text": "\n"},
                            {"type": "Plain", "text": "未知指令\n"}])
        else:
            if 'ACTV_cm' in ENV and ENV['ACTV_cm']:
                tr = ENV['cm'].search(rd['sender']['group']['id'], msg)
                res.extend(tr)
        return res
