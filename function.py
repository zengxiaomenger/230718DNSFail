#process.py
import os
import csv
import json
import data
from easyfunc import ip2asnum,judge_success,fqdn2sld
from tqdm import tqdm
def dns_QorR(QorR):
    if QorR=='0':
        data.Num_query+=1
    else:
        data.Num_response+=1
def dns_Rstatus(Rstatus):
    if Rstatus in data.Dic_state:
        data.Dic_state[Rstatus]+=1
    else:
        data.Dic_state[Rstatus]=0

def dns_Fail(Qname,Qtype,Resolver,Rjson):
    #但凡有查询就记录下来
    data.Num_query_all+=1
    #对不同查询类型的记录
    if Qtype in data.Dic_record_num_all:
        data.Dic_record_num_all[Qtype]+=1
    else:
        data.Dic_record_num_all[Qtype]=1
        #这里注意！！！success同时统计
        data.Dic_record_num_success[Qtype]=0
    #对不同查询域名的记录
    if Qtype==1:
        data.Num_query_a_all+=1
        if Qname in data.Dic_domain_num_a_all:
            data.Dic_domain_num_a_all[Qname]+=1
        else:
            data.Dic_domain_num_a_all[Qname]=1
            data.Dic_domain_num_a_success[Qname]=0
    elif Qtype==28:
        data.Num_query_aaaa_all+=1
        if Qname in data.Dic_domain_num_aaaa_all:
            data.Dic_domain_num_aaaa_all[Qname]+=1
        else:
            data.Dic_domain_num_aaaa_all[Qname]=1
            data.Dic_domain_num_aaaa_success[Qname]=0
    #对不同解析器的记录
    if Resolver in data.Dic_resolver_num_all:
        data.Dic_resolver_num_all[Resolver]+=1
    else:
        data.Dic_resolver_num_all[Resolver]=1
        data.Dic_resolver_num_success[Resolver]=0
        #ip2asnum
        data.Dic_resolver_asnum[Resolver]=ip2asnum(Resolver)

    if Qtype==1:
        if Resolver in data.Dic_resolver_num_a_all:
            data.Dic_resolver_num_a_all[Resolver]+=1
        else:
            data.Dic_resolver_num_a_all[Resolver]=1
            data.Dic_resolver_num_a_success[Resolver]=0
    elif Qtype==28:
        if Resolver in data.Dic_resolver_num_aaaa_all:
            data.Dic_resolver_num_aaaa_all[Resolver]+=1
        else:
            data.Dic_resolver_num_aaaa_all[Resolver]=1
            data.Dic_resolver_num_aaaa_success[Resolver]=0
    
    #下面再判断是否成功
    Rdic=json.loads(Rjson)
    success=judge_success(Rdic['rr'],Qname,Qtype)
    if success==1:
        data.Num_query_success+=1
        #记录类型
        data.Dic_record_num_success[Qtype]+=1
        #域名 解析器
        data.Dic_resolver_num_success[Resolver]+=1
        if Qtype==1:
            data.Num_query_a_success+=1
            data.Dic_domain_num_a_success[Qname]+=1
            data.Dic_resolver_num_a_success[Resolver]+=1
        elif Qtype==28:
            data.Num_query_aaaa_success+=1
            data.Dic_domain_num_aaaa_success[Qname]+=1
            data.Dic_resolver_num_aaaa_success[Resolver]+=1

def dns_ClientQuery(Client,Rstatus,Qtype,Qname):
    #client查询数量
    if Client in data.Dic_client_query_num:
        data.Dic_client_query_num[Client]+=1
    else:
        data.Dic_client_query_num[Client]=1
    #client查询返回状态
    if Client not in data.Dic_client_Rstatus_dic:
        data.Dic_client_Rstatus_dic[Client]={}
    if Rstatus in data.Dic_client_Rstatus_dic[Client]:
        data.Dic_client_Rstatus_dic[Client][Rstatus]+=1
    else:
        data.Dic_client_Rstatus_dic[Client][Rstatus]=1
        
    #client查询类型
    if Client not in data.Dic_client_Qtype_dic:
        data.Dic_client_Qtype_dic[Client]={}
    if Qtype in data.Dic_client_Qtype_dic[Client]:
        data.Dic_client_Qtype_dic[Client][Qtype]+=1
    else:
        data.Dic_client_Qtype_dic[Client][Qtype]=1
        
    #client查询域名
    if Client not in data.Dic_client_domain_dic:
        data.Dic_client_domain_dic[Client]={}
    if Qname in data.Dic_client_domain_dic[Client]:
        data.Dic_client_domain_dic[Client][Qname]+=1
    else:
        data.Dic_client_domain_dic[Client][Qname]=1
        

def dns_NXDomain(Qname):
    #统计NXDomain信息
    if Qname in data.Dic_nxdomain_num:
        data.Dic_nxdomain_num[Qname]+=1
    else:
        data.Dic_nxdomain_num[Qname]=1
    sld=fqdn2sld(Qname)
    if sld in data.Dic_nxsld_num:
        data.Dic_nxsld_num[sld]+=1
    else:
        data.Dic_nxsld_num[sld]=1

def dns_newgTLD(Qname):
    #判断new gTLD
    TLD=Qname.rsplit('.',1)[-1]
    if TLD in data.List_newgTLDs:
        data.Num_newgTLDs+=1

def process():
    dir_in='./source_data'
    file_names=os.listdir(dir_in)
    for file_name in tqdm(file_names):#对于每个源文件
        if file_name=='.DS_Store':
            continue
        file_in_path=os.path.join(dir_in,file_name)
        #输入的文件对象
        file_in=open(file_in_path,'r',encoding='utf-8-sig')
        csv_in=csv.reader(file_in)
        i=0
        for line in csv_in:#对于每一行数据!!!!!
            i+=1
            if i>1000000:
                break
            Manmade =   line[7]
            Client  =   line[24]
            Resolver=   line[33]
            QorR    =   line[113]#0是query 1是response
            Rstatus =   line[119]#响应状态0 No Error 3 NXDomain
            Qname   =   line[124]
            Qtype   =   int(line[125])#该响应的查询种类 （数字类型
            Rjson   =   line[129]
            if Manmade=='31':#无视所有自造流量 不管qr
                data.Num_manmade+=1
                continue
            dns_QorR(QorR)  #统计查询/响应的数量
            if QorR=='0':#是查询
                pass
            elif QorR=='1':#是R 即响应
                dns_Rstatus(Rstatus)    #统计响应状态情况
                dns_newgTLD(Qname)      #new gTLD情况
                #用户查询数量、Rstatus各自数量、Qtype各自数量、domain各自数量
                dns_ClientQuery(Client,Rstatus,Qtype,Qname)
                if Rstatus=='0':#统计论文中fail情况
                    dns_Fail(Qname,Qtype,Resolver,Rjson)
                elif Rstatus=='3':#统计NXDomain情况
                    dns_NXDomain(Qname)
        # break