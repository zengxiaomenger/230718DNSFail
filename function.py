#process.py
import os
import csv
from dns_fun import *
from tqdm import tqdm

def process():
    dir_in='./source_data'
    file_names=os.listdir(dir_in)
    for file_name in tqdm(file_names):#对于每个源文件
        if file_name=='.DS_Store':
            continue
        # if file_name!='DNSdata_13.csv':
        #     continue
        file_in_path=os.path.join(dir_in,file_name)
        #输入的文件对象
        file_in=open(file_in_path,'r',encoding='utf-8-sig')
        csv_in=csv.reader(file_in)
        i=0
        for line in csv_in:#对于每一行数据!!!!!
            i+=1
            if i>1000000:
                break
            EorI    =   line[3]#69是向外，73是向内
            SorD    =   line[4]#12是单向流，3是双向流
            Manmade =   line[7]#人造流量
            Client  =   line[24]#用户ip
            Resolver=   line[33]#解析器ip
            DiaID   =   line[112]#dns事务ID 判断有多少个会话
            QorR    =   line[113]#0是query 1是response
            Rstatus =   line[119]#响应状态0 No Error 3 NXDomain
            Qname   =   line[124]
            Qtype   =   int(line[125])#该响应的查询种类 （数字类型
            Rjson   =   line[129]
            if Manmade=='31':#无视所有自造流量 不管qr
                data.Num_manmade+=1
                continue
            dns_DialogID(DiaID)#判断dns会话id
            dns_DIR(EorI,SorD)#统计流向以及是否有回应
            #再加一个判断所有域名中的public suffix与非public suffix
            #####想想怎么弄
            ##不然就先完善功能，这个再想想
            dns_QorR(QorR)  #统计查询/响应的数量
            if QorR=='0':#是查询
                pass
            elif QorR=='1':#是R 即响应
                dns_Rstatus(Rstatus)    #统计响应状态情况
                dns_Rtype(Qname,Qtype,Rstatus,Rjson)             #统计响应种类情况的分析
                
                dns_ClientQuery(Client,Rstatus,Qtype,Qname) #用户查询数量、Rstatus各自数量、Qtype各自数量、domain各自数量
                dns_newgTLD(Qname)      #new gTLD情况

                if Rstatus=='0':#统计论文中fail情况
                    dns_Fail(Qname,Qtype,Resolver,Rjson)
                elif Rstatus=='3':#统计NXDomain情况
                    dns_NXDomain(Qname)
        # break