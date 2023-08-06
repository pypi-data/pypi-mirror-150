import json
import os
from typing import Counter
import xlwings as xw
import shutil
from tqdm import tqdm
import datetime
from interval import Interval
import pandas as pd

class BzttExcl:  #工单处理
    log_lv = 3

    app=""
    wb = {}
    # def __init__(self, system_info, oltInfo, soft_ware_info):
    def  __init__(self,system_info={}):
        log_lv_data = {
            "ALL": 0,
            "TRACE": 1,
            "DEBUG": 2,
            "INFO": 3,
            "WARN": 4,
            "ERROR": 5,
            "FATAL": 6,
            "OFF": 7,
        }
        log_level = system_info.get("logLevel","INFO")
        json_title = system_info.get("title","无标题")
        json_description = system_info.get("description","无描述")

        self.log_lv = log_lv_data[log_level]
        print_data = [
            {"text": "json信息", "color": "33"},
            {"text": "json标题：" +  json_title, "color": "33"},
            {"text": "json描述：" +  json_description, "color": "33"},
            {"text": "配置文件版本：" + system_info["version"], "color": "33"}
        ]
        self.print_log(print_data, "INFO")

    def __del__(self):

        print ("")

        '''
        #time.sleep(1)
        for wdInfo in self.wb:
            print("关闭并保存:",wdInfo)
            self.wb[wdInfo].save()
            #time.sleep(2)
            self.wb[wdInfo].close()
        self.app.quit()
        '''
    # 显示信息
    def print_log(self, log_lv_info, log_lv_num):
        log_lv_data = {
            "ALL": 0,
            "TRACE": 1,
            "DEBUG": 2,
            "INFO": 3,
            "WARN": 4,
            "ERROR": 5,
            "FATAL": 6,
            "OFF": 7,
        }
        log_lv = log_lv_data[log_lv_num.upper()]

        if log_lv >= self.log_lv:
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "\033[1;%sm%s\033[0m" % ("34", "[" + log_lv_num.upper() + "]"))

            for info in log_lv_info:
                info.setdefault("end", "\n")

                print("\033[1;%sm%s\033[0m" % (info["color"], info["text"]), end=info["end"])


    # excel 判断表格内容（ifs）
    def ifsData(self,jsonData):
        screen = "=IFS("
        for conditionInfo in jsonData["condition"]:
            if conditionInfo["type"] == "exist":
                #print("exist",conditionInfo)
                screenInfo = "OR(COUNTIF('[%s]%s'!%s,{" % (conditionInfo["sourceFile"],conditionInfo["sourceShell"],conditionInfo["Range"])
                for info in conditionInfo["sourceData"]:
                    screenInfo = screenInfo + "\"" + info + "\","
                screen = screen +screenInfo[:-1] + "})),\"" + conditionInfo["targetData"] + "\","
            if conditionInfo["type"] == "countifs":
                #print("countifs",conditionInfo)
                #COUNTIFS([20211102_待装池.xls]待调度工单!$E:$E,Q29),"待装池12"
                screenInfo = "COUNTIFS('[%s]%s'!%s:%s,%s),\"%s\"," % (conditionInfo["sourceFile"],conditionInfo["sourceShell"],conditionInfo["Range"],conditionInfo["Range"],conditionInfo["sourceData"],conditionInfo["targetData"])
                screen = screen + screenInfo
            if conditionInfo["type"] == "end":
                screenInfo = "1,\"%s\","%(conditionInfo["targetData"])
                screen = screen + screenInfo
        screen = screen[:-1] + ")" 
        # print("screen_debug",screen)

        sht = self.wb[jsonData["sourceTitle"]].sheets(jsonData["sourceShell"])
        info = sht.used_range
        nrows = info.last_cell.row
        ncolumns = info.last_cell.column
        # print("nrows",nrows,"ncolumns",ncolumns)

        # print("正在计算请稍后...")
        sht.range(jsonData["startRangeCol"] + jsonData["startRangeRow"]).value = screen
        rangeEndStr = jsonData["startRangeCol"] + str(nrows)
        sourceRange = sht.range(jsonData["startRangeCol"] + jsonData["startRangeRow"]).api
        fillRange = sht.range(jsonData["startRangeCol"] + jsonData["startRangeRow"] + ':' + rangeEndStr).api
        
        print_data = [
            {"text": "计算公式：" + screen, "color": "34"},

        ]
        self.print_log(print_data, "DEBUG")

        print_data = [
            {"text": "判断函数（ifs）", "color": "33"},
            {"text": "操作表格： [%s]%s!%s%s:%s" % (jsonData["sourceTitle"],jsonData["sourceShell"],jsonData["startRangeCol"],jsonData["startRangeRow"],rangeEndStr ), "color": "34"},
            {"text": "正在计算中，请稍后...", "color": "33"}

        ]
        self.print_log(print_data, "INFO")
        sourceRange.AutoFill(fillRange, 0)

    # 新建Shell
    def addShell(self,jsonData):
        # print("新建Shell",jsonData)
        print_data = [
            {"text": "新建Shell,请稍后...", "color": "33"},
            {"text": "[%s]%s,{%s}" % (jsonData["sourceTitle"],jsonData["after"],jsonData["targetShell"]), "color": "33"}

        ]
        self.print_log(print_data, "INFO")
        sht =  self.wb[jsonData["sourceTitle"]].sheets.add(jsonData["targetShell"], after=jsonData["after"])
    
    # 筛选数据，计算数量，列
    def countyCountyNum(self,jsonData):
        #print("jsonData",jsonData)
        print_data = [
            {"text": "正在筛选数据，计算数量，请稍后...", "color": "33"}

        ]
        self.print_log(print_data, "INFO")

        #生成专用  =SUM(COUNTIFS(
        screen = "=SUM(COUNTIFS("
        for conditionInfo in jsonData["condition"]:
            if conditionInfo["type"] == "exist":
                screenInfo = "'[%s]%s'!$%s1:$%s65536,{" % (jsonData["sourceFile"],jsonData["sourceShell"],conditionInfo["Range"],conditionInfo["Range"])
                for info in conditionInfo["data"]:
                    screenInfo = screenInfo + "\"" + info + "\","
                screen = screen +screenInfo[:-1] + "}," 
            elif conditionInfo["type"] == "timeRange":
               
                # print("conditionInfo",conditionInfo["data"])
                #if conditionInfo["data"]["start"]["disable"] == "false": #处理开始

                for timeInfo in conditionInfo["data"]:
                    screenInfo = "'[%s]%s'!$%s1:$%s65536," % (jsonData["sourceFile"],jsonData["sourceShell"],conditionInfo["Range"],conditionInfo["Range"])

                    if "Reformat" in timeInfo:
                        Reformat = timeInfo["Reformat"]
                    else:
                        Reformat = '%Y-%m-%d %H:%M:%S'

                    startTimeStr = timeInfo["data"]
                    SourceTimeStr = datetime.datetime.strptime(str(startTimeStr),timeInfo["dataFormat"])  + datetime.timedelta(days = int(timeInfo["num"]))
                    startTimeStr = SourceTimeStr.strftime( timeInfo["type"] + Reformat )   #'>%Y-%m-%d %H:%M:%S'
                    screenInfo = screenInfo + "\"" + startTimeStr + "\","
                    #print("screenInfo",screenInfo)
                    screen = screen +screenInfo[:-1] + "," 
                #循环赋值
        #print("screen",screen)
 
        data = {}
        log_data_tmp = ""
        #生成
        for info in jsonData["county"]:
            #print("countyCountyNum",info)
            screenInfoFor = ""
            for value in info["value"]:
                #print("value",value)
                screenInfo = r"'[%s]%s'!$%s1:$%s65536,{" % (jsonData["sourceFile"],jsonData["sourceShell"],value["Range"],value["Range"])
                screenInfo = screenInfo + "\"" + value["Regular"] + "\","
                screenInfoFor = screenInfoFor + screenInfo[:-1] + "},"
                #print("screenInfo",screenInfo)
                
            data[info["title"]] = screen + screenInfoFor[:-1] + "))" 
            log_data_tmp = log_data_tmp + info["title"] + " : " + screen + screenInfoFor[:-1] + "))" + "\n\n"
        
        print_data = [
            {"text": "筛选表格", "color": "33","end":"："},
            {"text": "[%s]%s" % (jsonData["targetTitle"],jsonData["targetShell"]), "color": "34","end":"\n"},

            {"text": "写入起始位置", "color": "33","end":"\n"},
            {"text": "[%s]%s!%s%s" % (jsonData["targetTitle"],jsonData["targetShell"],jsonData["targetRange"]["startLetter"],jsonData["targetRange"]["startNum"]), "color": "34"},

        ]
        self.print_log(print_data, "INFO")

        print_data = [
            {"text": "筛选条件", "color": "33","end":"\n"},
            {"text": log_data_tmp, "color": "34"},
        ]
        self.print_log(print_data, "DEBUG")

        i = int(jsonData["targetRange"]["startNum"])
        sht = self.wb[jsonData["targetTitle"]].sheets(jsonData["targetShell"])
        
        for info in data:
            rang = jsonData["targetRange"]["startLetter"]+ str(i)
            sht.range(rang).formula = data[info]#单元格赋值
            i = i +1

        return

    def RemoveDuplicates(self,jsonData):

        print_str_copy = "[%s]%s!%s:%s,{%s}" % (jsonData["sourceTitle"],jsonData["sourceShell"],jsonData["sourceRange"]["start"],jsonData["sourceRange"]["end"],jsonData["RemoveNum"])
        print_data = [
            {"text": "删除重复项", "color": "33"},
            {"text": print_str_copy, "color": "33"},

        ]
        self.print_log(print_data, "INFO")

        shtSource = self.wb[jsonData["sourceTitle"]].sheets(jsonData["sourceShell"])

        shtSource.range(jsonData["sourceRange"]["start"],jsonData["sourceRange"]["end"]).api.RemoveDuplicates(int(jsonData["RemoveNum"]))
    # 初始化数据 （格式化数据）
    def InitJson(self,formatJson):
        formatJsonStr =json.dumps(formatJson,ensure_ascii=False)   #转换字符串

        for i in range(0,len(formatJson["formatVariable"])):
            formatJsonStr =json.dumps(formatJson,ensure_ascii=False)   #转换字符串
            fucInfoJson = formatJson["formatVariable"]
            info = fucInfoJson[i]
            in_value = info["value"]

            if info["type"] == "input":
                # in_value = {}
                title = in_value.get("title","请输入：")
                inputIntStr = input(title)
                formatJsonStr = formatJsonStr.replace(info["name"],inputIntStr)

            #字符串转换
            elif info["type"] == "replace":
                #print("json:",info["value"])
                in_type = in_value.get("type","str")
                if in_type == "str":
                    valueStr = in_value["data"]
                elif in_type == "json":
                    valueStr = json.dumps(info["value"]["data"],ensure_ascii=False) 
                else:
                    raise Exception("未知替换类型")
                
                formatJsonStr = formatJsonStr.replace( "\"" + info["name"] + "\"",valueStr)
            
            # 时间替换
            elif info["type"] == "time":

                in_value = {
                    "in_data":in_value["inData"],                   #输入时间
                    "in_format":in_value.get("inFormat","%Y%m%d"), # 输入时间格式,
                    "out_format":in_value.get("outFormat","%Y%m%d"), # 输出时间格式,
                    "change_num":in_value.get("changeNum","%Y%m%d"), # 变化数量,
                    "change_unit":in_value.get("changeUnit","%Y%m%d"), # 变化单位,
                }
                target_time_str = self._change_time(in_value)
                formatJsonStr = formatJsonStr.replace( "\"" + info["name"] + "\"",target_time_str)
                
            elif info["type"] == "date2Rang":
                # print("date2Rang:",info["value"])
                #str转time
                SourceTimeStr = datetime.datetime.strptime(str(info["value"]["dateStr"]),info["value"]["dateFormat"])
                year = SourceTimeStr.year
                month = SourceTimeStr.month
                day = SourceTimeStr.day
                # print("SourceTimeStr",SourceTimeStr,year,month,day)
                for RangeFormatInfo in info["value"]["RangeFormat"]:
                    # print("RangeFormatInfo",RangeFormatInfo)
                    chengeStr = 0
                    #输出B1
                    if RangeFormatInfo["type"] == "day":
                        chengeStr = int(day)
                    elif RangeFormatInfo["type"] == "month":
                        chengeStr = int(month)
                    elif RangeFormatInfo["type"] == "year":
                        chengeStr = int(year)
                    zoom_2_5 = Interval(RangeFormatInfo["Range"][0], RangeFormatInfo["Range"][1])
                    
                    #在区间内
                    if chengeStr in zoom_2_5:
                        if RangeFormatInfo["direction"] == "column":
                            #字母转转数字 columnInitial
                            columnInitial = self.Col2Int(RangeFormatInfo["columnInitial"])
                            columnTial = columnInitial + chengeStr
                            columnStr = self.ExcelColumn(columnTial - RangeFormatInfo["Range"][0])
                            chengeAll = columnStr +  RangeFormatInfo["rowInitial"]
                            # print("chengeAll",chengeAll)
                            formatJsonStr = formatJsonStr.replace(info["name"],chengeAll)
                            break
            #重置
            formatJson = json.loads(formatJsonStr)
        data = json.loads(formatJsonStr)
        return data
   
    # 复制数据
    def copyData(self,copyJson):
        print_str_copy = "[%s]%s!%s" % (copyJson["sourceTitle"],copyJson["sourceShell"],copyJson["sourceRange"]["start"] + ":" + copyJson["sourceRange"]["end"])
        
        print_str_paste = "[%s]%s!{ " % (copyJson["targetTitle"],copyJson["targetShell"])
        for info in copyJson["targetRange"]:
            print_str_paste = print_str_paste + info["start"] + ", "
        print_str_paste = print_str_paste[:-1] + "}"

        print_data = [
            {"text": "复制数据", "color": "33"},
            {"text": print_str_copy, "color": "33","end":" --> "},
            {"text": print_str_paste, "color": "33"}
        ]
        self.print_log(print_data, "INFO")

        shtSource = self.wb[copyJson["sourceTitle"]].sheets(copyJson["sourceShell"])
        shtTarget = self.wb[copyJson["targetTitle"]].sheets(copyJson["targetShell"])
        rangSource = copyJson["sourceRange"]["start"] + ":" + copyJson["sourceRange"]["end"]
        shtSource.range(rangSource).copy(destination=None)

        for pasteInfo in copyJson["targetRange"]:
            rangTarget = pasteInfo["start"]
            shtTarget.range(rangTarget).paste(paste="values_and_number_formats")


        '''
        copyDataTmp = shtSource.range(rangSource).value
        print("copyDataTmp",copyDataTmp)
        print("rangTarget",rangTarget)
        #sht.range('A1').options(transpose=True).value=[1,2,3]
        shtTarget.range(rangTarget).options(transpose=True).value = copyDataTmp
        '''

    def ExcelColumn(self,n:int)->str:
        num = [chr(i) for i in range(65,91)]
        ret,(n,m) = '',divmod(n-1,26)
        if n: ret += self.ExcelColumn(n)
        ret += num[m]
        return ret
    
    def Col2Int(self,s:str)->int:
        ret=0
        ret += (ord(s[0])-64)*26**(len(s)-1)
        s = s[1:]
        if s: ret += self.Col2Int(s)
        return ret

    # 格式化数据（初始）
    def formatJson(self,formatJson):
        print_data = [
            {"text": "开始格式化数据", "color": "33"}
        ]
        self.print_log(print_data, "INFO")

        formatJsonStr =json.dumps(formatJson,ensure_ascii=False)   #转换字符串
        
        for i in range(0,len(formatJson["formatVariable"])):
            formatJsonStr =json.dumps(formatJson,ensure_ascii=False)   #转换字符串
            fucInfoJson = formatJson["formatVariable"]
            info = fucInfoJson[i]

            print_data = [
                {"text": "格式化类型：", "color": "34","end":" "},
                {"text": info["type"] , "color": "33"},

                {"text": "格式化数据：", "color": "33","end":" "},
                {"text": info, "color": "34"},
            ]
            self.print_log(print_data, "DEBUG")

            if info["type"] == "input":
                titleTmp = info.get("title","请输入：")
                inputIntStr = input(titleTmp)
                #inputIntStr = "20211102"
                formatJsonStr = formatJsonStr.replace(info["name"],inputIntStr)

                #字符串转换
            elif info["type"] == "json":
                #print("json:",info["value"])
                valueStr = json.dumps(info["value"],ensure_ascii=False) 
                formatJsonStr = formatJsonStr.replace( "\"" + info["name"] + "\"",valueStr)
                #print("formatJsonStr:",formatJsonStr)
            elif info["type"] == "time":
                startTimeStr = str(info["value"])
                SourceTimeStr = datetime.datetime.strptime(startTimeStr,info["valueFormat"])  + datetime.timedelta(days = int(info["num"]))
                startTimeStr = SourceTimeStr.strftime( info["format"] )   #'>%Y-%m-%d %H:%M:%S'
                formatJsonStr = formatJsonStr.replace( "\"" + info["name"] + "\"",startTimeStr)

            elif info["type"] == "date2Rang":
                #print("date2Rang:",info["value"])
                #str转time
                SourceTimeStr = datetime.datetime.strptime(str(info["value"]["dateStr"]),info["value"]["dateFormat"])
                year = SourceTimeStr.year
                month = SourceTimeStr.month
                day = SourceTimeStr.day
                #print("SourceTimeStr",SourceTimeStr,year,month,day)
                for RangeFormatInfo in info["value"]["RangeFormat"]:
                    #print("RangeFormatInfo",RangeFormatInfo)
                    chengeStr = 0
                    #输出B1
                    if RangeFormatInfo["type"] == "day":
                        chengeStr = int(day)
                    elif RangeFormatInfo["type"] == "month":
                        chengeStr = int(month)
                    elif RangeFormatInfo["type"] == "year":
                        chengeStr = int(year)

                    zoom_2_5 = Interval(RangeFormatInfo["Range"][0], RangeFormatInfo["Range"][1])
                    
                    #在区间内
                    if chengeStr in zoom_2_5:
                        if RangeFormatInfo["direction"] == "column":
                            #字母转转数字 columnInitial
                            columnInitial = self.Col2Int(RangeFormatInfo["columnInitial"])
                            columnTial = columnInitial + chengeStr
                            columnStr = self.ExcelColumn(columnTial - RangeFormatInfo["Range"][0])
                            chengeAll = columnStr +  RangeFormatInfo["rowInitial"]
                            #print("chengeAll",chengeAll)
                            formatJsonStr = formatJsonStr.replace(info["name"],chengeAll)
                            break

            #重置
            formatJson = json.loads(formatJsonStr)
        data = json.loads(formatJsonStr)
        return data
    
    # 打开文件
    def openfile(self,iniFile):        
        print_data = [
            {"text": "正在复制文件，请稍后...", "color": "33"}
        ]
        self.print_log(print_data, "INFO")

        #检测文件是否存在

        #复制文件,并重命名
        for fileInfo in iniFile["info"]:
            print_data = [
                {"text": fileInfo["sourcePath"] + fileInfo["name"] + "." + fileInfo["suffix"], "color": "33","end":" --> "},
                {"text": fileInfo["targetPath"] + fileInfo["name"] + "_" + fileInfo["title"] + "." + fileInfo["suffix"], "color": "33"},
            ]
            self.print_log(print_data, "INFO")

            shutil.copyfile(fileInfo["sourcePath"] + fileInfo["name"] + "." + fileInfo["suffix"], fileInfo["targetPath"] + fileInfo["name"] + "_" + fileInfo["title"] + "." + fileInfo["suffix"])

        print_data = [
            {"text": "文件复制完毕", "color": "33"}
        ]
        self.print_log(print_data, "INFO")

        print_data = [
                {"text": "正在打开文件,请稍后...", "color": "33"},
        ]
        self.print_log(print_data, "INFO")
        # 格式化app
        appConfig = iniFile.get("appConfig",{})
        visibleFlag = appConfig.get("visible",True)
        add_book = appConfig.get("addBook",False)
        display_alerts = appConfig.get("displayAlerts",False)

        self.app = xw.App(visible=visibleFlag,add_book=add_book)

        self.app.display_alerts=display_alerts
        
        #打开文件
        for fileInfo in iniFile["info"]:
            print_data = [
                {"text": fileInfo["title"], "color": "33","end":" - "},
                {"text": fileInfo["targetPath"] + fileInfo["name"] + "_" + fileInfo["title"] + "." + fileInfo["suffix"], "color": "33"},

            ]
            self.print_log(print_data, "INFO")

            #self.wb[fileInfo["title"]] =  xw.Book(fileInfo["path"] + fileInfo["name"] + "_" + fileInfo["title"] + "." + fileInfo["suffix"]) #创建一个新的Excel文件
            self.wb[fileInfo["title"]] =  self.app.books.open(fileInfo["targetPath"] + fileInfo["name"] + "_" + fileInfo["title"] + "." + fileInfo["suffix"]) #创建一个新的Excel文件
        
        
        print_data = [
            {"text": "文件打开完毕", "color": "33"}
        ]
        self.print_log(print_data, "INFO")
        #校验 文件
 
    # 格式化筛选数据
    def _handle_list_filters(self, args_filters):
        """
        处理list接口传入的过滤条件
        :param args_filters: 传入过滤条件
        :return: 转换后的sqlalchemy过滤条件
        """
        query_str = ""
        if args_filters:
            for item in args_filters:
                query_str = query_str + " and "
                item_type = item.get("type","str")
                value = ""
                # 判断数据类型
                if item_type == "time": # 转为时间格式
                    # 2019-06-1
                    for info in item["value"]:
                        in_value = {
                            "in_data":info["data"],
                            "in_format":info["dataFormat"],
                            "out_format":"%Y-%m-%d",
                            "change_num":info["change_num"],
                            "change_unit":info["change_unit"],
                        }
                        value_tmp = self._change_time(in_value)
                        value = value  +item["range_name"] + info["type"] + "'" + value_tmp + "' and "
                    value = value[:-4]
                    pass
                elif item_type == "str":
                    value = str(item["value"])
                    pass
                elif item_type == "int":
                    value = int(item["value"])
                # 生成数据
                if item["condition"] == '=':
                    query_str = query_str + item["range_name"] + " == " + value 
                elif item_type == 'time':
                    query_str = query_str + value 
                

        query_str = query_str[4:]
        return query_str
    
    def _getFilterData(self,dfData,inData):
        for info in inData:
            range_name = info["range_name"]
            info_value = info["value"]
            if info["type"] == "array":
                if info["condition"] == "in":
                    dfData = dfData[dfData[info["range_name"]].isin(info_value)]
                elif info["condition"] == "not in":
                    dfData = dfData[~dfData[info["range_name"]].isin(info_value)]
                else:
                    raise Exception("筛选条件错误")
            elif info["type"] == "time":

                startTime = self._change_time(info_value[0])
                endTime = self._change_time(info_value[1])
                dfData = dfData[(dfData[range_name] >= startTime) & (dfData[range_name] <= endTime)]
            elif info["type"] == "regex": #正则筛选   
                if info["condition"] == "in": # 包含
                    Bool = dfData[range_name].str.contains(info_value)
                    dfData = dfData[Bool]
                elif info["condition"] == "not in":# 删除
                    Bool = dfData[range_name].str.contains(info_value)
                    dfData = dfData[~Bool]
                else:
                    raise Exception("筛选条件错误")
            else:
                raise Exception("未知类型。")

        return dfData

        pass

    # 高级筛选  
    def AdvancedFilter(self,inData):
        # 写入筛选条件
        sourceRange = inData["sourceRange"]
        args_filters = inData["query"]
        countRange = inData["countRange"] # 统计数量参数
        sourceSht = self.wb[sourceRange["sourceTitle"]].sheets(sourceRange["sourceShell"])
        # 读取数据 
        print_data = [
            {"text": "正在读取数据，请稍后..." , "color": "33"}
        ]
        self.print_log(print_data, "INFO")
        sourceData=sourceSht.range('A:BW').options(pd.DataFrame,header=1,index=False,expand='table').value
        print_data = [
            {"text": "读取成功，正在处理数据..." , "color": "33"}
        ]
        self.print_log(print_data, "INFO")
        # 生成筛选字符串
        df_data_all=pd.DataFrame([])
        query_str_all = ""
        # 循环生成数据
        for info in args_filters:
            df_data_tmp = self._getFilterData(sourceData,info)
            df_data_all=pd.concat([df_data_all,df_data_tmp])
        # 删除重复项
        df_data_all = df_data_all.drop_duplicates(keep="first")
        print_data = [
            {"text": "处理成功，筛选出 " + str(len(df_data_all)) + " 条数据" , "color": "33"},
            {"text": "正在记录明细... ", "color": "33"}
        ]
        self.print_log(print_data, "INFO")
        # 循环写入明细数据
        for details_range_info in inData["detailsRange"]:
            df_data_all_columns = details_range_info.get("columns",df_data_all.columns)
            self.wb[details_range_info["targetTitle"]].sheets(details_range_info["targetShell"]). \
                range(details_range_info["targetRange"]["startLetter"] + str(details_range_info["targetRange"]["startNum"])) \
                    .value=df_data_all[df_data_all_columns].set_index(df_data_all_columns[0])

        print_data = [
            {"text": "明细记录成功 " , "color": "33"},
            {"text": "正在计算每种数量... ", "color": "33"}
        ]
        self.print_log(print_data, "INFO")

        # 循环计算数量
        for countRange_info in countRange:  
            # 分别计算区县数量
            countyQuery = countRange_info["countyQuery"]  # 区县筛选条件
            countyArrayTmp = []
            show_info = []
            for countyQuery_info in countyQuery: # 分别计算区县数量
                numData = str(len(self._getFilterData(df_data_all,countyQuery_info["value"])))
                countyArrayTmp = countyArrayTmp + [numData]
                show_one = {countyQuery_info.get("title","无"):numData}
                show_info  = show_info +[show_one]
                pass
            # 写入内容 
            print_data = [
                {"text": "统计数量结果 : " + str(show_info), "color": "33"},
            ]
            self.print_log(print_data, "INFO")

            directionTmp = countRange_info.get("direction","column")
            if directionTmp =="row":
                flagTmp = False
            elif directionTmp =="column":
                flagTmp = True

            self.wb[countRange_info["targetTitle"]].sheets(countRange_info["targetShell"]). \
                range(countRange_info["targetRange"]["startLetter"] + str(countRange_info["targetRange"]["startNum"])). \
                        options(transpose=flagTmp).value=countyArrayTmp

    # 更改时间
    def _change_time(self,in_value):
        startTimeStr = str(in_value["in_data"]) # 输入时间
        in_format = in_value.get("in_format","%Y%m%d") # 输入时间格式
        out_format = in_value.get("out_format","%Y%m%d") # 输出时间格式
        change_num = int(in_value.get("change_num",0)) # 变化数量
        change_unit = in_value.get("change_unit","day") # 变化单位

        if change_unit == "day":
            SourceTimeStr = datetime.datetime.strptime(startTimeStr,in_format)  + datetime.timedelta(days = change_num)
        else:
            raise Exception("未知变化类型")
        startTimeStr = SourceTimeStr.strftime( out_format )   #'>%Y-%m-%d %H:%M:%S'
        return startTimeStr

    # 整体执行操作
    def performOperate(self,operate_json):
        for info in operate_json:
            if info["type"] == "advancedFilter": # 高级筛选
                print_data = [
                    {"text": "执行高级筛选：" + info.get("title","无描述"), "color": "33"}
                ]
                self.print_log(print_data, "INFO")
                self.AdvancedFilter(info["value"])
            if info["type"] == "screening":
                self.countyCountyNum(info)
            if info["type"] == "copy":
                self.copyData(info)
            if info["type"] == "ifs":
                self.ifsData(info)
            if info["type"] == "addShell":
                self.addShell(info)
            if info["type"] == "RemoveDuplicates":
                self.RemoveDuplicates(info)
        pass

   

