import os

module_lst = os.listdir('./plugin')
for i in module_lst:
    name = i.split('.')
    if name[-1] == 'py':
        __import__(f"plugin.{name[0]}")
