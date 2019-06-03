import atexit
from pyVim import connect
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vmodl
from pyVmomi import vim
import ssl
import time

def GetVMHosts(content):
    host_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                        [vim.HostSystem],
                                                        True)
    obj = [host for host in host_view.view]
    host_view.Destroy()
    return obj

def save_vmstats(memorySize,overallMemoryUsage,Max_cpu,overallCpuUsage,Numvm,NumHost,NumVmDisk,Numvmconnect,Numvmhealth,Numconnect,Numhealth):
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
    sql = "insert into presitation(time, memorySize,overallMemoryUsage,Max_cpu,overallCpuUsage,Numvm,NumHost,NumVmDisk,Numvmconnect,Numvmhealth,Numconnect,Numhealth) values ('%s','%.2f','%.2f','%.2f','%.2f','%.2f','%.2f','%.2f','%.2f','%.2f','%.2f','%.2f')"%(time,memorySize,overallMemoryUsage,Max_cpu,overallCpuUsage,Numvm,NumHost,NumVmDisk,Numvmconnect,Numvmhealth,Numconnect,Numhealth)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()



def main():
        memorySize = 0
        overallMemoryUsage = 0
        Max_cpu = 0
        overallCpuUsage = 0
        Numvm = 0
        NumHost = 0
        NumVmDisk = 0
        Numvmconnect = 0
        Numvmhealth = 0
        Numconnect = 0
        Numhealth = 0

        while True:
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
            NumHost = len(hosts)
            for host in hosts:
                memorySize += int(int(host.summary.hardware.memorySize)/(1024*1024*1024))
                Max_cpu += int(host.summary.hardware.cpuMhz)*int(host.summary.hardware.numCpuCores)
            for host in hosts:
                if host.summary.quickStats.overallMemoryUsage:
                    overallMemoryUsage += int(host.summary.quickStats.overallMemoryUsage/1024)
                if host.summary.quickStats.overallCpuUsage:
                    overallCpuUsage += int(host.summary.quickStats.overallCpuUsage)
                if host.runtime.connectionState == 'connected':
                    Numconnect += 1
                if host.summary.overallStatus == 'green':
                    Numhealth += 1
            container = content.rootFolder  # starting point to look into
            viewType = [vim.VirtualMachine]  # object types to look for
            recursive = True  # whether we should look into it recursively
            containerView = content.viewManager.CreateContainerView(
                container, viewType, recursive)
            children = containerView.view
            Numvm = len(children)
            for vm in children:
                NumVmDisk += int(vm.summary.config.numVirtualDisks)
                if vm.runtime.connectionState == 'connected':
                    Numvmconnect += 1
                if vm.summary.overallStatus == 'green':
                    Numvmhealth += 1
            save_vmstats(memorySize,overallMemoryUsage,Max_cpu,overallCpuUsage,Numvm,NumHost,NumVmDisk,Numvmconnect,Numvmhealth,Numconnect,Numhealth)
            time.sleep(3600)
if __name__ == "__main__":
    main()
exit()
