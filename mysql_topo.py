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


def add_topo(ID,Ip,Name,Type):
    # add
    sql = "insert into topo(id,ip,name,type) values(%s,%s,%s,%s)" % (ID,"'"+ Ip + "'" ,"'" + Name + "'","'" + Type + "'")
    #param = (ID,Ip,Name,Type)
    my_connect()  # 打开链接
    cursor.execute(sql)
    cursor.close()
    conn.close()
        # conn.rollback()


def update_topo(dictory):
    # 更新
    my_connect()
    sql = "update topo set "
    flag = 0
    if "ip" in dictory:
        flag = 1
        sql += "ip = '%s'" %(dictory["ip"])
    if "name" in dictory:
        if flag == 1:
            sql += ",name = '%s'" %(dictory["name"])
        else:
            flag = 1
            sql += "name = '%s'" %(dictory["name"])
    if "type" in dictory:
        if flag == 1:
            sql += ",type = '%s'" %(dictory["type"])
        else:
            flag = 1
            sql += "type = '%s'" %(dictory["type"])
    sql += " where id = %d" %(dictory["id"])
        
    #sql = "update topo set ip='%s',name='%s',type='%s' where id='%d'" % (Ip,Name,Type,ID)
    try:
        cursor.execute(sql)
        cursor.close()
        conn.close()
    except StandardError as e:
        print("更新数据异常", e)


def Select_topo(dictory):
    # 查询
    my_connect()
    if 'type' in dictory:
        if dictory['type'] == 'total':
            cursor.execute("SELECT * from topo")
        else:
            cursor.execute("SELECT * from topo where type ='%s'"% dictory['type'])
    elif 'ip' in dictory:
        cursor.execute("SELECT * from topo where ip = '%s'" % dictory['ip'])
    else:
        cursor.execute("SELECT * from topo where id =%d" % dictory['id'])
    data = cursor.fetchall()
        #for row in data:
            # 注意int类型需要使用str函数转义
            #print('id: ', row[0], '  name: ', row[1], ' age ', row[2])
        # 提交事务
    cursor.close()  # 关闭游标
    conn.close()  # 释放数据库资源
    return data


def delete_topo(ID):
    # 删除
    my_connect()
    sql = "delete from topo where id='%d'" % (ID)
    # parama =(ID)
    cursor.execute(sql)
    cursor.close()
    conn.close()

#add_topo(0,"''",'G-第二块光纤板','fiber')



