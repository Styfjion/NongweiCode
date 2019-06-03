from config1 import *
info = alarm('config.ini')
info.cfg_load()
a = 5
key = str(a)
print(info.cfg_dump('Event_level')[key])
