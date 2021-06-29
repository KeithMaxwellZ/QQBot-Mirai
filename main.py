from p_var import ENV, DEBUG
import mirai_socket as ms
import addon
import plugin
import DM

from pprint import pprint

if __name__ == '__main__':
    pprint(ENV['cmd'])
    ms.run()

