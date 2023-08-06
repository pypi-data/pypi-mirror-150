
import sys
# print(sys.path)
sys.path.append('D:\\彭升智\\git\\bztt-excl\\bztt_excl')

# '/home/user/fqm/'为示例的项目路径，换成你的即可

import json

import os
import sys

from bzttExcl import BzttExcl


versioNum = "0.0.5"

if __name__=='__main__': 
    try:

        print("程序版本:",versioNum)
        
        print("读取配置文件...")
        json_data = {}
        with open('./text.json','r',encoding='utf8')as fp:
            json_data = json.load(fp)
            #print('这是文件中的json数据：',json_data)
            print('标题:',json_data["title"])
        print("校验配置文件...")
        
        system_info = {
            "log_level":"ALL"
        }
        BzExcl1 = BzttExcl(system_info)
        
        #格式化数据
        json_data = BzExcl1.formatJson(json_data)
        #print("设置配置文件...",json_data)
        iniFile = json_data["openFlie"]
        # os.system("pause")
        
        #打开文件
        print("打开文件...")
        # a = BzExcl1.openfile(iniFile) #打开文件
        print("处理数据...")
       

        for info in json_data["operate"]:
            
            if info["type"] == "screening":
                BzExcl1.countyCountyNum(info)
            if info["type"] == "copy":
                BzExcl1.copyData(info)
            if info["type"] == "ifs":
                print("info",info)
                BzExcl1.ifsData(info)
            if info["type"] == "addShell":
                print("info",info)
                BzExcl1.addShell(info)
            if info["type"] == "RemoveDuplicates":
                print("RemoveDuplicates",info)
                BzExcl1.RemoveDuplicates(info)
        del BzExcl1
        print("运行结束...")
        os.system("pause")
        sys.exit(1)
    except Exception as e:
        print("运行异常:",e)
        del BzExcl1
        print("运行异常:",e)
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


   

