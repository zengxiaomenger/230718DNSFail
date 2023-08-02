#process.py
import os
import csv
import json
import data
import awdb
from tqdm import tqdm

def judge_recursive(Rdic_rr,Rname,Qname):
    if Rname==Qname:
        return 1
    else:
        tp=0
        for Ritem in Rdic_rr:
            if Ritem['type']==5 and Ritem['cname']==Rname:
                tp=judge_recursive(Rdic_rr,Ritem['name'],Qname)
                if tp==1:
                    break
        return tp

def judge_success(Rdic_rr,Qname,Qtype):
    #复杂的判别方法是正着找，我们反着找！
    success=0
    # if Qtype!=1 and Qtype!=28:#不可能出现递归
    #     for Ritem in Rdic_rr:#直接找
    #         if Ritem['name']==Qname and Ritem['type']==Qtype:
    #             success=1
    # else: #是1或28
    for Ritem in Rdic_rr:#对于所有的答案
        if Ritem['type']==Qtype:
            if judge_recursive(Rdic_rr,Ritem['name'],Qname)==1:
                success=1
                break
        if success==1:
            break
    return success

def ip2asnum(str_ip):
    reader=awdb.open_database(r'./other_data/IP_basic_single_WGS84.awdb')
    (record,prefix_len)=reader.get_with_prefix_len(str_ip)
    ans=record.get('asnumber').decode('utf8')
    if ans!='':
        return ans
    else:
        return 'null'

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
            if i>100000:
                break
            Manmade =   line[7]
            Resolver=   line[33]
            QorR    =   line[113]#0是query 1是response
            Rstatus =   line[119]#响应状态0 No Error 3 NXDomain
            Qname   =   line[124]
            Qtype   =   int(line[125])#该响应的查询种类 （数字类型
            Rjson   =   line[129]

            if Manmade=='31':#无视所有自造流量 不管qr
                data.Num_manmade+=1
                continue
            if QorR=='1':#是R 即响应
                #统计响应状态情况 
                dns_Rstatus(Rstatus)
                if Rstatus=='0':#统计论文中fail情况
                    dns_Fail(Qname,Qtype,Resolver,Rjson)
                #new gTLD情况
                dns_newgTLD(Qname)
        break