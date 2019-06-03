import datetime
def Select():
    import pymysql
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='1qazXSW@_xyz!',
        db='agr_data',
        charset="utf8")
    cur = conn.cursor()
    
    
    begin = (datetime.datetime.now()-datetime.timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')
    end = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = "select t.sip, t.dip, t.log_type, t.event_type, t.counts from (select t1.sip sip, t1.dip dip, t1.log_type log_type, t1.event_type event_type, count(*) counts from \
                                    (select * from seclog where time>'%s' and time<'%s') t1 group by sip, dip, log_type) \
                                    t order by t.counts desc limit 0, 10" % (begin, end)
    cur.execute(sql)
    Results = cur.fetchall()
            
    OutInfo = []
    dic = {}
    for r in Results:
        sip = r[0]
        dip = r[1]
        log_type = r[2]
        event_type = r[3]
        counts = r[4]

        dic_key = sip + ',' + dip
        if(dic_key not in dic):
            dic.setdefault(dic_key, []).append(log_type)
            dic.setdefault(dic_key, []).append(counts)
        else:
            if(log_type not in dic[dic_key]):
                dic.setdefault(dic_key, []).append(log_type)
                dic.setdefault(dic_key, []).append(counts)
                
    attack1 = []
    attack2 = []
    attack3 = []
    attack4 = []
    for key in dic:
        if(len(dic[key]) == 2):
            attack1.append([key, dic[key][0], dic[key][1]])
            
        if(len(dic[key]) == 4):
            sumCount = 0
            for i in range(1, 4, 2):
                sumCount += dic[key][i]
            temp = [key]
            for j in range(4):
                temp.append(dic[key][i])
            temp.append(sumCount)  
            attack2.append(temp)
            
        if(len(dic[key]) == 6):
            sumCount = 0
            for i in range(1, 6, 2):
                sumCount += dic[key][i]
            temp = [key]
            for j in range(6):
                temp.append(dic[key][i])
            temp.append(sumCount)  
            attack3.append(temp)

        if(len(dic[key]) == 8):
            sumCount = 0
            for i in range(1, 8, 2):
                sumCount += dic[key][i]
            temp = [key]
            for j in range(8):
                temp.append(dic[key][i])
            temp.append(sumCount)  
            attack4.append(temp)

    attack1 = sorted(attack1,key=(lambda x:x[-1]),reverse=True)
    attack2 = sorted(attack2,key=(lambda x:x[-1]),reverse=True)
    attack3 = sorted(attack3,key=(lambda x:x[-1]),reverse=True)
    attack4 = sorted(attack4,key=(lambda x:x[-1]),reverse=True)
    if(len(attack1)>0):
        print(attack1[0])
    if(len(attack2)>0):
        print(attack2[0])
    if(len(attack3)>0):
        print(attack3[0])
    if(len(attack4)>0):
        print(attack4[0])
Select()
