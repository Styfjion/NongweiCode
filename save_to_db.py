import pymysql
from config1 import*

global conn
global cur
global Host
global Passwd
global User
global Port
global DB

def read_db_config():
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
    read_db_config()
    conn = pymysql.connect(
        host=Host,
        port=Port,
        user=User,
        passwd=Passwd,
        db=DB,
        charset="utf8")
    cur = conn.cursor()
    
def firewall(time, level, eventtype, sip, sport, dip, dport, msg):
    connectMySQL()
    sql = "insert into firewall(time, level, eventtype, sip, sport, dip, dport, msg) values ('%s','%d','%s','%s','%s','%s','%s','%s')"\
          %(time, level, eventtype, sip, sport, dip, dport, msg)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def ips(time, danger_degree, breaking_sighn, event, src_addr, src_port, dst_addr, dst_port, user, smt_user, proto):
        connectMySQL()
        sql = "insert into ips(time, danger_degree, breaking_sighn, event, src_addr, src_port, dst_addr, dst_port, user, smt_user, proto) \
               values ('%s','%d','%d','%s','%s','%s','%s','%s','%s','%s','%s')"\
               %(time, danger_degree, breaking_sighn, event, src_addr, src_port, dst_addr, dst_port, user, smt_user, proto)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

def waf(time, severity_id, msg_id, method, url, post, dip,hostname, dport, sip, sport, user_agent, tag_id, action_id,\
                         response_code, matchs, rule_id, unique_id, country, province, city):
        connectMySQL()
        sql = "insert into waf(time, severity_id, msg_id, method, url, post, dip,hostname, dport, sip, sport, user_agent, tag_id, action_id,\
               response_code, matchs, rule_id, unique_id, country, province, city) values ('%s','%d','%s','%s','%s','%s','%s','%s','%s','%s','%s',\
               '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
               %(time, severity_id, msg_id, method, url, post, dip,hostname, dport, sip, sport, user_agent, tag_id, action_id,\
               response_code, matchs, rule_id, unique_id, country, province, city)
        #print(sql)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

def Tamper_protection(time, level, eventtype, sip, sport, dip, dport, msg):
    connectMySQL()
    sql = "insert into Tamper_protection(time, level, eventtype, sip, sport, dip, dport, msg) values ('%s','%d','%s','%s','%s','%s','%s','%s')"\
          %(time, level, eventtype, sip, sport, dip, dport, msg)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def others(ip, data):
    connectMySQL()
    sql = "insert into others(ip, data) values ('%s','%s')" % (ip, data)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()



