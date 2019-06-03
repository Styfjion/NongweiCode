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
    print(ip, MSG)
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
    print(ip, MSG)
    sql = "insert into ips(ip, msg) values ('%s','%s')"%(ip, MSG)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


firewall_ip = "192.168.2.175"
firewall_data = "Jun 28 15:05:29 2508313174001641(root) 46083623 Traffic@FLOW: NAT: 192.168.22.58:54848->114.114.114.114:53(UDP), snat to 101.95.111.66:54848, vr trust-vr, user -@UNKNOWN, host -, rule 2"
#save_firewall(firewall_ip, firewall_data)

ips_ip = "192.168.2.173"
ips_data = "time:2018-06-28 14:53:48;danger_degree:2;breaking_sighn:0;event:[41357]HTTP请求伪造参数规避尝"
save_ips(ips_ip, ips_data)

waf_ip = "192.168.2.174"
waf_data = "Jun 28 14:48:44 localhost DBAppWAF: happentime/2018-06-28 14:48:41,severity_id/3,msg_id/16020,method/GET,url/www.shac.gov.cn/backup.tar,post/,dip/116.228.18.39,hostname/www.shac.gov.cn,dport/80,sip/112.65.228.2,sport/39199"
save_waf(waf_ip, waf_data)


