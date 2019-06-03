def save_eventlog(time, ip, severname, eventtype, level, descript):
    import pymysql

    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='1qazXSW@_xyz!',
        db='agr_data',
        charset="utf8")

    cur = conn.cursor()
    sql = "insert into eventlog(time, ip, eventname, eventtype, level, descript) values('%s','%s','%s','%s','%s','%s')"\
          %(time, ip, severname, eventtype, level, descript)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
