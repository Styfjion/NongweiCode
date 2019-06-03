#!/usr/bin/env python
import socket
import save_to_db
import datetime

syslog_serverty={  0:"紧急",
                   1:"警报",
                   2:"严重",
                   3:"错误",
                   4:"警告",
                   5:"提醒",
                   6:"信息",
                   7:"debug"
                 }
syslog_facility={  0:"kernel",
                   1:"user",
                   2:"mail",
                   3:"daemaon",
                   4:"auth",
                   5:"syslog",
                   6:"lpr",
                   7:"news",
                   8:"uucp",
                   9:"cron",
                   10:"authpriv",
                   11:"ftp",
                   12:"ntp",
                   13:"security",
                   14:"console",
                   15:"cron",
                   16:"local 0",
                   17:"local 1",
                   18:"local 2",
                   19:"local 3",
                   20:"local 4",
                   21:"local 5",
                   22:"local 6",
                   23:"local 7"
                 }

firewall_ip = "192.168.2.175"
ips_ip = "192.168.2.173"
waf_ip = "192.168.2.174"

address=('',514)
try:
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(address)
except:
    print("error bind!")
 
while 1:
    try:
        data,addr=s.recvfrom(20480)
        if not data:
            break
        
        data = str(data, encoding='utf8')
        addr = str(addr)
        ip = addr[2:15]  #判别日志来源
        
        if(ip == firewall_ip):
            #提取PRI部分
            PRI_right = data.find('>')
            PRI = data[1:PRI_right]
            PRI = int(PRI)
            Severity = PRI & 7
            #Facility = PRI >> 3
            MSG = data[20:]
            nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') #现在
            save_to_db.save_firewall_data(nowTime,syslog_serverty[Severity], MSG)
            
        if(ip == ips_ip):
            PRI_right = data.find('>')
            PRI = data[1:PRI_right]
            PRI = int(PRI)
            serverty = syslog_serverty[PRI]
            
            MSG_left = PRI_right + 1
            MSG = data[MSG_left:]
            MSG_list = MSG.split(';')
            time = ""
            danger_degree = ""
            breaking_sighn = ""
            event = ""
            src_addr = ""
            src_port = ""
            dst_addr = ""
            dst_port = ""
            user = ""
            smt_user = ""
            proto = ""
            #print (MSG_list)
            for msg in MSG_list:
                index = msg.find(':')
                if(msg[:index] == "time"):
                    time_index = index + 1
                    time = msg[time_index :]
                if(msg[:index] == "danger_degree"):
                    danger_index = index + 1
                    danger_degree = msg[danger_index :]
                if(msg[:index] == "breaking_sighn"):
                    breaking_index = index + 1
                    breaking_sighn = msg[breaking_index :]
                if(msg[:index] == "event"):
                    event_index = index + 1
                    event = msg[event_index :]
                if(msg[:index] == "src_addr"):
                    src_addr_index = index + 1
                    src_addr = msg[src_addr_index :]
                if(msg[:index] == "src_port"):
                    src_port_index = index + 1
                    src_port = msg[src_port_index :]
                if(msg[:index] == "dst_addr"):
                    dst_addr_index = index + 1
                    dst_addr = msg[dst_addr_index :]
                if(msg[:index] == "dst_port"):
                    dst_port_index = index + 1
                    dst_port = msg[dst_port_index :]
                if(msg[:index] == "user"):
                    user_index = index + 1
                    user = msg[user_index :]
                if(msg[:index] == "smt_user"):
                    smt_user_index = index + 1
                    smt_user = msg[smt_user_index :]
                if(msg[:index] == "proto"):
                    proto_index = index + 1
                    proto = msg[proto_index :]
            save_to_db.save_ips_data(time, danger_degree, breaking_sighn, event, src_addr, src_port, dst_addr, dst_port, user, smt_user, proto)

        if(ip == waf_ip):
            MSG = data[25:]
            MSG_list = MSG.split(',')
            #print(MSG_list)
            time = ""
            severity_id = ""
            msg_id = ""
            method = ""
            url = ""
            post = ""
            dip = ""
            hostname = ""
            dport = ""
            sip = ""
            sport = ""
            user_agent =""
            tag_id = ""
            action_id = ""
            response_code = ""
            matchs = ""
            rule_id = ""
            unique_id = ""
            country = ""
            province = ""
            city = ""
            for msg in MSG_list:
                index = msg.find('/')
                if("happentime" in msg[:index]):
                    time_index = index + 1
                    time = msg[time_index :]
                if(msg[:index] == "severity_id"):
                    severity_id_index = index + 1
                    severity_id = msg[severity_id_index :]
                if(msg[:index] == "msg_id"):
                    msg_id_index = index + 1
                    msg_id = msg[msg_id_index :]
                if(msg[:index] == "method"):
                    method_index = index + 1
                    method = msg[method_index :]
                if(msg[:index] == "url"):
                    url_index = index + 1
                    url = msg[url_index :]
                if(msg[:index] == "post"):
                    post_index = index + 1
                    #post = msg[post_index :]
                if(msg[:index] == "dip"):
                    dip_index = index + 1
                    dip = msg[dip_index :]
                if(msg[:index] == "hostname"):
                    hostname_index = index + 1
                    hostname = msg[hostname_index :]
                if(msg[:index] == "dport"):
                    dport_index = index + 1
                    dport = msg[dport_index :]
                if(msg[:index] == "sip"):
                    sip_index = index + 1
                    sip = msg[sip_index :]
                if(msg[:index] == "sport"):
                    sport_index = index + 1
                    sport = msg[sport_index :]
                if(msg[:index] == "user_agent"):
                    user_agent_index = index + 1
                    user_agent = msg[user_agent_index :]
                if(msg[:index] == "tag_id"):
                    tag_id_index = index + 1
                    tag_id = msg[tag_id_index :]
                if(msg[:index] == "action_id"):
                    action_id_index = index + 1
                    action_id = msg[action_id_index :]
                if(msg[:index] == "response_code"):
                    response_code_index = index + 1
                    response_code = msg[response_code_index :]
                if(msg[:index] == "match"):
                    matchs_index = index + 1
                    matchs = msg[matchs_index :]
                if(msg[:index] == "unique_id"):
                    unique_id_index = index + 1
                    unique_id = msg[unique_id_index :]
                if(msg[:index] == "country"):
                    country_index = index + 1
                    country = msg[country_index :]
                if(msg[:index] == "province"):
                    province_index = index + 1
                    province = msg[province_index :]
                if(msg[:index] == "city"):
                    city_index = index + 1
                    city = msg[city_index :]
            save_to_db.save_waf_data(time, severity_id, msg_id, method, url, post, dip,\
                                     hostname, dport, sip, sport, user_agent, tag_id, action_id,\
                                     response_code, matchs, rule_id, unique_id, country, province, city)
        
    except:
        print("recvfrom error!")
        break
        
    
#f.close()
try:
    s.close()
except:
    print("close error")
