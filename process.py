#process.py
import os
import csv
import pandas as pd
from tqdm import tqdm
from dns_fun import *
from output import output6
def process_sort_QR():#排序所有事务ID，检查QR占比
    file_name=data.dir_in+'/2023-08-31-DNS.csv'
    print('reading source data...')
    #下面这个要对应准
    dfin=pd.read_csv(file_name,usecols=[24,33,112,113,119,124,125],\
                        names=['Client','Resolver','DiaID','QorR','Rcode','Qname','Qtype'],\
                        )
    print('extracting data to dataframe...')
    #这个决定新的csv里面前后顺序
    Dic_item={}
    Dic_item['index']=[]
    Dic_item['DiaID']=[]
    Dic_item['QorR']=[]
    Dic_item['Rcode']=[]
    Dic_item['Qname']=[]
    Dic_item['Qtype']=[]
    Dic_item['Client']=[]
    Dic_item['Resolver']=[]
    for index,line in tqdm(dfin.iterrows()):
        #这个顺序无所谓
        Dic_item['index'].append(index)
        Dic_item['DiaID'].append(line['DiaID'])
        Dic_item['QorR'].append(line['QorR'])
        Dic_item['Rcode'].append(line['Rcode'])
        Dic_item['Qname'].append(line['Qname'])
        Dic_item['Qtype'].append(line['Qtype'])
        Dic_item['Client'].append(line['Client'])
        Dic_item['Resolver'].append(line['Resolver'])
    print('sorting dataframe...')
    dfout=pd.DataFrame(Dic_item)
    dfout_sorted=dfout.sort_values(by=['DiaID','index'])
    print('caculating dialogs...')
    #这里为了统计是01的各个属性做准备
    data.Dic_DialogQR01['Rcode']={}
    data.Dic_DialogQR01['Client']={}
    data.Dic_DialogQR01['Qname']={}
    data.Dic_DialogQR01['Qtype']={}
    data.Dic_DialogQR01['Rcode']['all']=0
    data.Dic_DialogQR01['Client']['all']=0
    data.Dic_DialogQR01['Qname']['all']=0
    data.Dic_DialogQR01['Qtype']['all']=0
    for index,line in tqdm(dfout_sorted.iterrows()):
        dns_DialogQR(line['Qname'],line['QorR'],line['Resolver'],line['Client'],line['Rcode'],line['Qtype'])
    output6()
    print('caculating dialogs over!')

def process():
    #处理其他的
    file_names=os.listdir(data.dir_in)
    for file_name in file_names:#对于每个源文件
        if file_name=='.DS_Store':
            continue
        if '23-08' in file_name:
            continue
        print(file_name)
        file_in_path=os.path.join(data.dir_in,file_name)
        #输入的文件对象
        file_in=open(file_in_path,'r',encoding='utf-8-sig')
        csv_in=csv.reader(file_in)
        i=0
        for line in tqdm(csv_in):#对于每一行数据!!!!!
            i+=1
            # if i>100000:
            #     break
            EorI    =   line[3]#69是向外，73是向内
            SorD    =   line[4]#12是单向流，3是双向流
            Manmade =   line[7]#人造流量
            Client  =   line[24]#用户ip
            Resolver=   line[33]#解析器ip
            DiaID   =   line[112]#dns事务ID 判断有多少个会话
            QorR    =   line[113]#0是query 1是response
            Rcode   =   line[119]#响应状态0 No Error 3 NXDomain
            Qname   =   line[124].lower()
            Qtype   =   int(line[125])#该响应的查询种类 （数字类型
            Rjson   =   line[129]
            if Manmade=='31':#无视所有自造流量 不管qr
                data.Num_manmade+=1
                continue
            dns_DIR(EorI,SorD)#统计流向以及是否有回应
            # #再加一个判断所有域名中的public suffix与非public suffix
            dns_QorR(QorR)  #统计查询/响应的数量
            # dns_sortQR(Client,Resolver,DiaID,QorR,Rcode,Qname,Qtype)
            if QorR=='0':#是查询
                pass
            elif QorR=='1':#是R 即响应
                dns_Rstatus(Rcode)    #统计响应状态情况
                dns_Rtype(Qname,Qtype,Rcode,Rjson)             #统计响应种类情况的分析
                dns_Rdomain(Qname,Rcode,Rjson)        #pubsuf 非pubsuf相关
                dns_Rresolver(Resolver,Rcode,Rjson)   #resolver处理状态相关
                dns_ClientQuery(Client,Rcode,Qtype,Qname) #用户查询数量、Rstatus各自数量、Qtype各自数量、domain各自数量
                dns_newgTLD(Qname)      #new gTLD情况
                if Rcode=='0':#统计论文中fail情况
                    # dns_Fail(Qname,Qtype,Resolver,Rjson)
                    pass
                elif Rcode=='3':#统计NXDomain情况
                    dns_NXDomain(Qname,Client)
        # break