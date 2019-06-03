def Select0():
    import pymysql
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='agr_data',
        charset="utf8")
    cur = conn.cursor()
    
    try:
        OutInfo = []
        sql = "select * from ips"
        cur.execute(sql)
        results = cur.fetchall()
        for r1 in results:
            Info = []
            for r2 in r1:
                Info.append(r2)
            OutInfo.append(Info)
        return OutInfo
    except:
        print("Error: Unable to fetch data!!!")

def Select1(sql):
    print (sql)
    import pymysql
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='agr_data',
        charset="utf8")
    cur = conn.cursor()
    
    try:
        OutInfo = []
        cur.execute(sql)
        results = cur.fetchall()
        for r1 in results:
            Info = []
            for r2 in r1:
                Info.append(r2)
            OutInfo.append(Info)
        #print (OutInfo)
        return OutInfo
    except:
        print("Error: Unable to fetch data!!!")
        
def IPS_list():
    try:
        Results = Select0()
        ret = []
        for i in range(len(Results)):
            Time = str(Results[i][0])
            danger_degree = Results[i][1]
            breaking_sighn= Results[i][2]
            event = Results[i][3]
            src_addr = Results[i][4]
            src_port = Results[i][5]
            dst_addr = Results[i][6]
            dst_port = Results[i][7]
            user = Results[i][8]
            smt_user = Results[i][9]
            proto = Results[i][10]
            data = {"Time":Time, "danger_degree":danger_degree, "breaking_sighn":breaking_sighn, "event":event,\
                    "src_addr":src_addr, "src_port":src_port, "dst_addr":dst_addr, "dst_port":dst_port,\
                    "user":user, "smt_user":smt_user, "proto":proto}
            ret.append(data)
        #print (ret)
    except:
        print("Count Error!!!")

def IPS_search(begin, end, danger_degree, breaking_sighn, event, src_addr, src_port, dst_addr, dst_port, user, smt_user, proto):
    try:
        sql = "select * from ips "
        flag = 0
        if(begin != "all"):
            if(flag == 0):
                sql += "where time>%s" %("'" + begin + "'")
                flag = 1
            else:
                sql += "and time>%s" %("'" + begin + "'")
        if(end != "all"):
            if(flag == 0):
                sql += "where time<%s" %("'" + end + "'")
                flag = 1
            else:
                sql += "and time<%s" %("'" + end + "'")
        if(danger_degree != "all"):
            if(flag == 0):
                sql += "where danger_degree=%s" %("'" + danger_degree + "'")
                flag = 1
            else:
                sql += "and danger_degree=%s" %("'" + danger_degree + "'")
        if(breaking_sighn != "all"):
            if(flag == 0):
                sql += "where breaking_sighn=%s" %("'" + breaking_sighn + "'")
                flag = 1
            else:
                sql += "and breaking_sighn=%s" %("'" + breaking_sighn + "'")
        if(event != "all"):
            if(flag == 0):
                sql += "where event=%s" %("'" + event + "'")
                flag = 1
            else:
                sql += "and event=%s" %("'" + event + "'")
        if(src_addr != "all"):
            if(flag == 0):
                sql += "where src_addr=%s" %("'" + src_addr + "'")
                flag = 1
            else:
                sql += "and src_addr=%s" %("'" + src_addr + "'")
        if(src_port != "all"):
            if(flag == 0):
                sql += "where src_port=%s" %("'" + src_port + "'")
                flag = 1
            else:
                sql += "and src_port=%s" %("'" + src_port + "'")
        if(dst_addr != "all"):
            if(flag == 0):
                sql += "where dst_addr=%s" %("'" + dst_addr + "'")
                flag = 1
            else:
                sql += "and dst_addr=%s" %("'" + dst_addr + "'")
        if(dst_port != "all"):
            if(flag == 0):
                sql += "where dst_port=%s" %("'" + dst_port + "'")
                flag = 1
            else:
                sql += "and dst_port=%s" %("'" + dst_port + "'")
        if(user != "all"):
            if(flag == 0):
                sql += "where user=%s" %("'" + user + "'")
                flag = 1
            else:
                sql += "and user=%s" %("'" + user + "'")
        if(smt_user != "all"):
            if(flag == 0):
                sql += "where smt_user=%s" %("'" + smt_user + "'")
                flag = 1
            else:
                sql += "and smt_user=%s" %("'" + smt_user + "'")
        if(proto != "all"):
            if(flag == 0):
                sql += "where proto=%s" %("'" + proto + "'")
                flag = 1
            else:
                sql += "and proto=%s" %("'" + proto + "'")
        
        Results = Select1(sql)
        ret = []
        for i in range(len(Results)):
            Time = str(Results[i][0])
            danger_degree = Results[i][1]
            breaking_sighn = Results[i][2]
            event = Results[i][3]
            src_addr = Results[i][4]
            src_port = Results[i][5]
            dst_addr = Results[i][6]
            dst_port = Results[i][7]
            user = Results[i][8]
            smt_user = Results[i][9]
            proto = Results[i][10]
            data = {"Time":Time, "danger_degree":danger_degree, "breaking_sighn":breaking_sighn, "event":event,\
                        "src_addr":src_addr, "src_port":src_port, "dst_addr":dst_addr, "dst_port":dst_port,\
                        "user":user, "smt_user":smt_user, "proto":proto}
            ret.append(data)
        print (ret)
    except:
        print("Count Error!!!")

def IPS_count_time_danger_degree(begin, end):
    import pymysql
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='agr_data',
        charset="utf8")
    cur = conn.cursor()
    
    try:
        OutInfo = []
        sql = "select t.danger_degree, t.counts from (select t1.danger_degree danger_degree, count(*) counts from \
                                            (select * from ips where time>%s and time<%s) t1 group by danger_degree) \
                                            t order by t.counts desc" % ("'" + begin + "'","'" + end + "'")
        cur.execute(sql)
        results = cur.fetchall()
        for r1 in results:
            Info = []
            for r2 in r1:
                Info.append(r2)
            OutInfo.append(Info)
        print (OutInfo)
    except:
        print("Error: Unable to fetch data!!!")

def IPS_count_time_src_addr(begin, end):
    
    import pymysql
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='agr_data',
        charset="utf8")
    cur = conn.cursor()
    
    try:
        OutInfo = []
        sql = "select t.src_addr, t.counts from (select t1.src_addr src_addr, count(*) counts from \
                                            (select * from ips where time>%s and time<%s) t1 group by src_addr) \
                                            t order by t.counts desc limit 0,10" % ("'" + begin + "'","'" + end + "'")
        cur.execute(sql)
        results = cur.fetchall()
        for r1 in results:
            Info = []
            for r2 in r1:
                Info.append(r2)
            OutInfo.append(Info)
        print (OutInfo)
    except:
        print("Error: Unable to fetch data!!!")
    
#IPS_list()
begin = "2018-07-03 14:20:30"
end = "2018-07-04 14:00:00"
danger_degree = '1'
breaking_sighn = "all"
event = "all"
src_addr = "all"
src_port = "all"
dst_addr = "all"
dst_port = "all"
user = "all"
smt_user = "all"
proto = "HTTP"
#IPS_search(begin, end, danger_degree, breaking_sighn, event, src_addr, src_port, dst_addr, dst_port, user, smt_user, proto)
IPS_count_time_danger_degree(begin, end)
IPS_count_time_src_addr(begin, end)







        
