# coding=utf-8

import pymysql

# MySQL相关设置
mysql_host = '127.0.0.1'
mysql_user = 'root'
mysql_passwd = '1qazXSW@_xyz!'
mysql_port = '3306'
mysql_database = 'agr_data'


def my_connect():
    """链接数据库"""

    global conn, cursor

    # print MySQLdb.version_info

    
    conn = pymysql.connect(host=mysql_host, user=mysql_user, passwd=mysql_passwd, charset='utf8', autocommit=True,
                               db=mysql_database)
    
    cursor = conn.cursor()


def select_event(dictory={}):
    # 查询
    my_connect()
    sql = "SELECT * from eventlog where "
    flag = 0
    if "begin" in dictory:
        flag = 1
        sql += "time>'%s'" % (dictory["begin"])
    if "end" in dictory:
        if flag == 1:
            sql += " and time<'%s'" % (dictory["end"])
        else:
            flag = 1
            sql += "time<'%s'" % (dictory["end"])
    if "ip" in dictory:
        if flag == 1:
            sql += " and ip = '%s'" % (dictory["ip"])
        else:
            sql += "ip = '%s'" % (dictory["ip"])
    if "eventname" in dictory:
        if flag == 1:
            sql += " and eventname = '%s'" % (dictory["eventname"])
        else:
            sql += "eventname = '%s'" % (dictory["eventname"])
    if "eventtype" in dictory:
        if flag == 1:
            sql += " and eventtype = '%s'" % (dictory["eventtype"])
        else:
            sql += "eventtype = '%s'" % (dictory["eventtype"])
    if dictory == {}:
        sql = 'SELECT * from eventlog'
    
        #for row in data:
            # 注意int类型需要使用str函数转义
            #print('id: ', row[0], '  name: ', row[1], ' age ', row[2])
        # 提交事务
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()  # 关闭游标
    conn.close()  # 释放数据库资源
    return data

def stats_eventlog(dictory):
    my_connect()
    if not "number" in dictory:
        number = 10
    else:
        number = dictory["number"]
    if "begin" in dictory and "end" in dictory:
        begin = dictory["begin"]
        end = dictory["end"]
        sql = "select t.ip, t.counts from (select t1.ip ip, count(*) counts from (select * from eventlog where time> \
              '%s' and time<'%s') t1 group by ip) t order by t.counts desc limit 0,%d"%(begin,end,number)
    elif "begin" in dictory:
        begin = dictory["begin"]
        sql = "select t.ip, t.counts from (select t1.ip ip, count(*) counts from (select * from eventlog where time> \
              '%s') t1 group by ip) t order by t.counts desc limit 0,%d"%(begin,number)
    elif "end" in dictory:
        end = dictory["end"]
        sql = "select t.ip, t.counts from (select t1.ip ip, count(*) counts from (select * from eventlog where \
              time<'%s') t1 group by ip) t order by t.counts desc limit 0,%d"%(end, number)
    else:
        sql = "select t.ip, t.counts from (select t1.ip ip, count(*) counts from (select * from eventlog) t1 group by ip) t order by t.counts desc limit 0,%d"%(number)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()  # 关闭游标
    conn.close()  # 释放数据库资源
    return data



