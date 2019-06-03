import datetime
from wechat_sender import *
sender  = Sender()
time = datetime.datetime.now()
sender.send(message='Hello,world!')