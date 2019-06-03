def waf_Select0():
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
        sql = "select * from waf"
        cur.execute(sql)
        results = cur.fetchall()
        for r1 in results:
            Info = []
            for r2 in r1:
                if(r2 == '\n'):
                    r2 = ''
                Info.append(r2)
            OutInfo.append(Info)
        return OutInfo
    except:
        print("Error: Unable to fetch data!!!")

def waf_list():
    try:
        Results = waf_Select0()
        ret = []
        for i in range(len(Results)):
            time = str(Results[i][0])
            severity_id = Results[i][1]
            msg_id= Results[i][2]
            method = Results[i][3]
            url = Results[i][4]
            post = Results[i][5]
            dip = Results[i][6]
            hostname = Results[i][7]
            dport = Results[i][8]
            sip = Results[i][9]
            sport = Results[i][10]
            user_agent = str(Results[i][11])
            tag_id = Results[i][12]
            action_id= Results[i][13]
            response_code = Results[i][14]
            matchs = Results[i][15]
            rule_id = Results[i][16]
            unique_id = Results[i][17]
            country = Results[i][18]
            province = Results[i][19]
            city = Results[i][20]
            data = {"Time":time, "severity_id":severity_id, "msg_id":msg_id, "method":method,"url":url, "post":post, "dip":dip, "hostname":hostname,\
                    "dport":dport, "sip":sip, "sport":sport,"user_agent":user_agent, "tag_id":tag_id, "action_id":action_id, "response_code":response_code,\
                    "matchs":matchs, "rule_id":rule_id, "unique_id":unique_id, "country":country,"province":province, "city":city}
            ret.append(data)
    except:
        print("Count Error!!!")
        
def waf_count_time_severity_id(begin, end):
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
        sql = "select t.severity_id, t.counts from (select t1.severity_id severity_id, count(*) counts from \
                                            (select * from waf where time>%s and time<%s) t1 group by severity_id) \
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

def waf_count_time_sip(begin, end):
    
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
        sql = "select t.sip, t.counts from (select t1.sip sip, count(*) counts from \
                                            (select * from waf where time>%s and time<%s) t1 group by sip) \
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

#waf_list()
begin = "2018-07-12 15:00:00"
end = "2018-07-14 00:00:00"
waf_count_time_severity_id(begin, end)
waf_count_time_sip(begin, end)




        
