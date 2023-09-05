#process.py
import os
import csv
import re
from tqdm import tqdm
from dns_fun import *

def process6():
    cnt_no=0
    #处理其他的
    file_names=os.listdir(data.dir_in)
    for file_name in file_names:#对于每个源文件
        if file_name=='.DS_Store':
            continue
        if file_name!='DNS_COLLECT_LOG.csv':
            continue
        file_in_path=os.path.join(data.dir_in,file_name)
        #输入的文件对象
        file_in=open(file_in_path,'r',encoding='utf-8-sig')
        csv_in=csv.reader(file_in)
        i=0
        for line in tqdm(csv_in):#对于每一行数据!!!!!
            i+=1
            # if i<685250:
            #     continue
            # if i>10000:
            #     break
            Client  =   line[11]#用户ip
            Resolver=   line[16]#解析器ip
            # DiaID   =   line[112]#dns事务ID 判断有多少个会话
            QorR    =   line[39]#0是query 1是response
            Rstatus =   line[45]#响应状态0 No Error 3 NXDomain
            Qname   =   line[48].lower()
            Qtype   =   int(line[46])#该响应的查询种类 （数字类型
            Rjson0  =   line[49].replace('\n','')
            if re.search("DNS_RR_TXT",line[49])==None:
                Rjson=str2json1(Rjson0)
            else:
                Rjson=str2json2(Rjson0)
            Rjson=Rjson.replace('\ufffd','')
            try:
                Rdic=json.loads(Rjson)
            except Exception:
                cnt_no+=1
                continue
            #再加一个判断所有域名中的public suffix与非public suffix
            dns_QorR(QorR)  #统计查询/响应的数量
            if QorR=='0':#是查询
                pass
            elif QorR=='1':#是R 即响应
                dns_Rstatus(Rstatus)    #统计响应状态情况
                dns_Rtype(Qname,Qtype,Rstatus,Rjson)             #统计响应种类情况的分析
                dns_Rdomain(Qname,Rstatus,Rjson)        #pubsuf 非pubsuf相关
                dns_Rresolver(Resolver,Rstatus,Rjson)   #resolver处理状态相关
                dns_ClientQuery(Client,Rstatus,Qtype,Qname) #用户查询数量、Rstatus各自数量、Qtype各自数量、domain各自数量
                dns_newgTLD(Qname)      #new gTLD情况
                if Rstatus=='0':#统计论文中fail情况
                    dns_Fail(Qname,Qtype,Resolver,Rjson)
                elif Rstatus=='3':#统计NXDomain情况
                    dns_NXDomain(Qname,Client)
    print('cnt_no '+str(cnt_no))
        # break