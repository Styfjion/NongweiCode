import socket
import Rawsave
import re
import datetime

address=('',514)
try:
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(address)
except:
    print("error bind!")
    
nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print (nowTime)
while 1:
    try:
        data,addr=s.recvfrom(10240)
        if not data:
            break
        try:
            #data = str(data, encoding='utf8')
            data = data.decode()
        except:
            continue
        
        addr = str(addr)
        ip = addr[2:15]  #判别日志来源
        #MSG = data[20:]
        p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        if not p.match(ip):
            continue
        if(ip == "192.168.2.175"):
            try:
                continue
                Rawsave.save_firewall(ip, str(data))
            except:
                data = data.replace("'","''")
                try:
                    Rawsave.save_firewall(ip, str(data))
                except:
                    print (ip, (data))
                    continue
        elif(ip == "192.168.2.174"):
            try:
                continue
                Rawsave.save_waf(ip, str(data))
            except:
                data = data.replace("'","''")
                Rawsave.save_waf(ip, str(data))
                print (ip, str(data))
        elif(ip == "192.168.2.173"):
            try:
                continue
                Rawsave.save_ips(ip, str(data))
            except:
                data = data.replace("'","''")
                Rawsave.save_ips(ip, str(data))
                print (ip, str(data))
        elif(ip == "116.228.18.37"):
            print(ip, str(data))
        else:
            try:
                continue
                Rawsave.save_others(str(ip), str(data))
            except:
                data = data.replace("'","''")
                Rawsave.save_others(str(ip), str(data))
                print (ip, str(data))
    except Exception as e:
        nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print (nowTime)
        print (Exception,":",e )   
        break
        
try:
    s.close()
except:
    print("close error")
