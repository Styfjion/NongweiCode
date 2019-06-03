def save_firewall(ip, MSG):
    import pymysql

    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='raw_data',
        charset="utf8")

    cur = conn.cursor()
    sql = "insert into firewall(ip, msg) values ('%s','%s')"%(ip, MSG)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    

def save_waf(ip, MSG):
    import pymysql

    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='raw_data',
        charset="utf8")

    cur = conn.cursor()
    #print(ip, MSG)
    sql = "insert into waf(ip, msg) values ('%s','%s')"%(ip, MSG)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def save_ips(ip, MSG):
    import pymysql

    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='raw_data',
        charset="utf8")

    cur = conn.cursor()
    #print(ip, MSG)
    sql = "insert into ips(ip, msg) values ('%s','%s')"%(ip, MSG)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def save_others(ip, MSG):
    import pymysql

    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='raw_data',
        charset="utf8")

    cur = conn.cursor()
    #print(ip, MSG)
    sql = "insert into others(ip, msg) values ('%s','%s')"%(ip, MSG)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
