import json
from easyfun import *

def dns_DialogID(now):#DNS会话数量
    if data.Num_dialog_preid!=now:
        data.Num_dialog+=1
    data.Num_dialog_preid=now

def dns_DIR(EorI,SorD):
    key=EorI+'_'+SorD
    if key in data.Dic_dir:
        data.Dic_dir[key]+=1
    else:
        data.Dic_dir[key]=1

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

def dns_Rtype(Qname,Qtype,Rstatus,Rjson):#注意这里Qtype是int
    if Qtype not in data.Dic_type_dic:
        #先不加fail，直接用那个
        data.Dic_type_dic[Qtype]={}
        data.Dic_type_dic[Qtype]['num_all']=0
        data.Dic_type_dic[Qtype]['num_no_error_data']=0
        data.Dic_type_dic[Qtype]['num_no_error_nodata']=0
        data.Dic_type_dic[Qtype]['num_nxdomain']=0
        data.Dic_type_dic[Qtype]['num_other_error']=0
        data.Dic_type_dic[Qtype]['set_fqdn']=set()
        data.Dic_type_dic[Qtype]['set_sld']=set()
        data.Dic_type_dic[Qtype]['set_tld']=set()
        data.Dic_type_dic[Qtype]['num_qdots']=0 #标签长度总数
        data.Dic_type_dic[Qtype]['num_pubsuf']=0

    data.Dic_type_dic[Qtype]['num_all']+=1
    #rcode相关
    if Rstatus=='0':
        Rdic=json.loads(Rjson)
        if Rdic['rr']!=[]:#不是空响应
            data.Dic_type_dic[Qtype]['num_no_error_data']+=1
        else:
            data.Dic_type_dic[Qtype]['num_no_error_nodata']+=1
    elif Rstatus=='3':
        data.Dic_type_dic[Qtype]['num_nxdomain']+=1
    else:#其他错误
        data.Dic_type_dic[Qtype]['num_other_error']+=1
    data.Dic_type_dic[Qtype]['set_fqdn'].add(Qname)
    data.Dic_type_dic[Qtype]['set_sld'].add(fqdn2sld(Qname))
    data.Dic_type_dic[Qtype]['set_tld'].add(fqdn2tld(Qname))
    data.Dic_type_dic[Qtype]['num_qdots']+=fqdn2qdots(Qname)
    if fqdn2pubsuf(Qname)!='null':
        data.Dic_type_dic[Qtype]['num_pubsuf']+=1

def dns_Rresolver(Resolver,Rstatus,Rjson):
    if Resolver not in data.Dic_resolver_dic:
        #先不加fail，直接用那个
        data.Dic_resolver_dic[Resolver]={}
        data.Dic_resolver_dic[Resolver]['num_all']=0
        data.Dic_resolver_dic[Resolver]['num_no_error_data']=0
        data.Dic_resolver_dic[Resolver]['num_no_error_nodata']=0
        data.Dic_resolver_dic[Resolver]['num_nxdomain']=0
        data.Dic_resolver_dic[Resolver]['num_other_error']=0

    data.Dic_resolver_dic[Resolver]['num_all']+=1
    #rcode相关
    if Rstatus=='0':
        Rdic=json.loads(Rjson)
        if Rdic['rr']!=[]:#不是空响应
            data.Dic_resolver_dic[Resolver]['num_no_error_data']+=1
        else:
            data.Dic_resolver_dic[Resolver]['num_no_error_nodata']+=1
    elif Rstatus=='3':
        data.Dic_resolver_dic[Resolver]['num_nxdomain']+=1
    else:#其他错误
        data.Dic_resolver_dic[Resolver]['num_other_error']+=1

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
       
def dns_newgTLD(Qname):
    #判断new gTLD
    TLD=Qname.rsplit('.',1)[-1]
    if TLD in data.List_newgTLDs:
        data.Num_newgTLDs+=1

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

def dns_NXDomain(Qname):
    #统计NXDomain信息
    if Qname in data.Dic_nxdomain_num:
        data.Dic_nxdomain_num[Qname]+=1
    else:
        data.Dic_nxdomain_num[Qname]=1

    #统计NXsld
    sld=fqdn2sld(Qname)
    if sld in data.Dic_nxsld_num:
        data.Dic_nxsld_num[sld]+=1
    else:
        data.Dic_nxsld_num[sld]=1

    #public_suffix
    #判断后缀长度增加，有没有在public_suffix里面出现过的
    pubsuf=fqdn2pubsuf(Qname)
    if pubsuf!='null':
        if pubsuf in data.Dic_nxpubsuf_num:
            data.Dic_nxpubsuf_num[pubsuf]+=1
        else:
            data.Dic_nxpubsuf_num[pubsuf]=1
