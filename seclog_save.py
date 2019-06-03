import pymysql
from config1 import*

global conn
global cur
global Host
global Passwd
global User
global Port
global DB

def readconfig():
    global Host
    global Passwd
    global User
    global Port
    global DB
    info = alarm('config.ini')
    info.cfg_load()
    dbdic = info.cfg_dump('log_db')
    Host = dbdic['log_dbhost']
    Passwd = dbdic['log_dbpwd']
    User = dbdic['log_dbusr']
    Port = int(dbdic['log_dbport'])
    DB = dbdic['log_dbname']
    

def connectMySQL():
    global conn
    global cur
    global Host
    global Passwd
    global User
    global Port
    global DB
    
    readconfig()
    
    conn = pymysql.connect(
        host=Host,
        port=Port,
        user=User,
        passwd=Passwd,
        db=DB,
        charset="utf8")
    cur = conn.cursor()
    
def save_seclog(time, level, logtype, eventtype, sip, sport, dip, dport, msg):
    global conn
    global cur
    connectMySQL()
    
    sql = "insert into seclog(time, level, log_type, event_type, sip, sport, dip, dport, msg)\
            values ('%s','%d','%s','%s','%s','%s','%s','%s','%s')"\
            %(time, level, logtype, eventtype, sip, sport, dip, dport, msg)
    try:
        #print (sql)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    except:
        print(sql)
    
'''

Host = '127.0.0.1'
Passwd = '1qazXSW@_xyz!'
User = 'root'
Port = 3306
DB = 'agr_data'

time = "2018-08-05 09:21:00"
level = "危险"
logtype = "防火墙"
eventtype = "fw_session"
sip = "110.123.4.66"
sport = ""
dip = "130.128.6.42"
dport = ""
msg = "ninhao"
save_seclog(time, level, logtype, eventtype, sip, sport, dip, dport, msg)
'''
