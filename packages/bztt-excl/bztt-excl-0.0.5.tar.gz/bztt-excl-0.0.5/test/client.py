
import sys
# print(sys.path)
sys.path.append('D:\\彭升智\\git\\bztt-excl\\bztt_excl')

# '/home/user/fqm/'为示例的项目路径，换成你的即可

import json
import os
import sys

from bzttExcl import BzttExcl
from __version__ import __version__
# from bztt_excl import BzttExcl

versioNum = "0.0.5"

if __name__=='__main__': 
    try:
        # print("测试",BzttExcl.versioNum)
        print("程序版本:",versioNum)
        print("模块版本:",__version__)
        
        json_data = {}
        with open('./text.json','r',encoding='utf8')as fp:
            json_data = json.load(fp)
            #print('这是文件中的json数据：',json_data)

        print("校验配置文件...")
        

        BzExcl1 = BzttExcl(json_data["jsonInfo"])
        
        #格式化数据
        json_data = BzExcl1.InitJson(json_data)
        
        #print("设置配置文件...",json_data)
        iniFile = json_data["openFlie"]
        # os.system("pause")
        
        #打开文件
        print("打开文件...")
        a = BzExcl1.openfile(iniFile) #打开文件
        print("处理数据...")

        # 执行操作
        BzExcl1.performOperate(json_data["operate"])

        del BzExcl1
        print("运行结束...")
        os.system("pause")
        sys.exit(1)
    except Exception as e:
        print("运行异常：",e)
        os.system("pause")
        sys.exit(1)
    #校验数据
    
    #循环操作
    '''
    BzExcl1 = BzExcl()
    #BzExcl1 = BzExcl()
    #a = BzExcl1.openfile(iniFile) #打开文件
    #循环配置
    a = BzExcl1.countyCountyNum(jsonData)  #统计数量
    #a = BzExcl1.copyData(copyJson) #复制数据
    #a = BzExcl1.advancedFilter(advancedFilterJson)#筛选数据

    '''


   

