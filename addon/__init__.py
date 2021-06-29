import os

# import all sub modules
module_lst = os.listdir('./addon')
for i in module_lst:
    name = i.split('.')
    if name[-1] == 'py':
        __import__(f"addon.{name[0]}")
