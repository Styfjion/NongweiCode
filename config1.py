#coding=utf-8
import configparser


class alarm(object):
    '''
1.dump ini
2.del section
3.del item
4.modify item
5.add section
6.save modify
'''

    def __init__(self, recordfile):
        # 文件名字
        self.logfile = recordfile
        self.cfg = configparser.ConfigParser()

    # 将文件load到cfg中
    def cfg_load(self):
        self.cfg.read(self.logfile)

    # 将写入内存中的内容显示出来（这些操作并不是在我们磁盘文件中的修改）
    def cfg_dump(self,section=''):
        se_list = self.cfg.sections()
        #print("===================>")
        dictory={}
        if not section:
            for item in se_list:
                dictory[item] = {}
                for value in self.cfg.items(item):
                    dictory[item][value[0]]=value[1]
            return dictory
        else:
            for value in self.cfg.items(section):
                    dictory[value[0]]=value[1]
            return dictory
           

    # 删除条目
    def delete_item(self, section, key):
        self.cfg.remove_option(section, key)

    # 删除section(课程)
    def delete_section(self, section):
        self.cfg.remove_section(section)

    # 添加一个section
    def add_section(self, section):
        self.cfg.add_section(section)

    # 添加和修改条目
    def set_item(self, section, key, value):
        self.cfg.set(section, key, value)

    def save(self):
        fp = open(self.logfile, 'w')
        self.cfg.write(fp)
        fp.close()


if __name__ == '__main__':
    info = alarm('config2.ini')
    info.cfg_load()
    print(info.cfg_dump('SwitchCPU'))
    '''
    info.delete_section('a')
    info.set_item('SwitchCPU', 'cpulevel1', '0.50')
    info.cfg_dump()
    info.save()
'''
# ini配置文件格式：
# 节：[session]
# 参数（键=值） name=value
# '''
