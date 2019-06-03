import atexit
from pyVim import connect
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vmodl
from pyVmomi import vim
import ssl
import time

def save_vmstats(cpurate, memoryrate):
    import datetime
    import pymysql
    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='1qazXSW@_xyz!',
        db='agr_data',
        charset="utf8")

    cur = conn.cursor()
    sql = "insert into vmstats(time, cpurate, memoryrate) values ('%s','%.4f','%.4f')"%(time, cpurate, memoryrate)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def GetVMHosts(content):
    host_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                        [vim.HostSystem],
                                                        True)
    obj = [host for host in host_view.view]
    host_view.Destroy()
    return obj

def main():
        memorySize = 0
        Max_cpu = 0
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        context.verify_mode = ssl.CERT_NONE
        serviceInstance = SmartConnect(host='200.0.0.52',
                                       user='jiaoda',
                                       pwd='1qazXSW@',
                                       port=443,
                                       sslContext=context)
        atexit.register(Disconnect, serviceInstance)
        content = serviceInstance.RetrieveContent()

        hosts = GetVMHosts(content)
        for host in hosts:
            memorySize += int(int(host.summary.hardware.memorySize)/(1024*1024))
            Max_cpu += int(host.summary.hardware.cpuMhz)*int(host.summary.hardware.numCpuCores)
        while True:
            time.sleep(60)
            overallMemoryUsage = 0
            overallCpuUsage = 0
            for host in hosts:
                if host.summary.quickStats.overallMemoryUsage:
                    overallMemoryUsage += int(host.summary.quickStats.overallMemoryUsage)
                if host.summary.quickStats.overallCpuUsage:
                    overallCpuUsage += int(host.summary.quickStats.overallCpuUsage)
            overallMemoryUsageRate = float('%.4f' %(overallMemoryUsage/memorySize))
            overallCpuUsageRate = float('%.4f' % (overallCpuUsage/Max_cpu))
            save_vmstats(overallCpuUsageRate, overallMemoryUsageRate) 
if __name__ == "__main__":
    main()
exit()
