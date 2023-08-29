#data.py
#以下有关输入输出
dir_in='./source_data_new'
dir_out='./result_data'
# 以下是有关数据统计的
#0
#dialog dir
Num_dialog=0
Num_dialog_preid='-1'#之前的会话id判断是否相同
#记录解析器处理不同DNS事务的QR数量占比
Num_resolver_Q=0
Num_resolver_R=0
Str_resolver_pre=''
Dic_resolver_QRdic={}
Dic_resolver_public_QRdic={}
Dic_dir={}#不同流方向的数量
#qr
Num_query=0
Num_response=0
#rcode manmade newgTLD
Dic_state={}
Num_manmade=0
Num_newgTLDs=0
List_newgTLDs=[]

List_country=[]
List_pubsuf=[]#公共后缀


# 以下是DNS Fail相关统计
Num_query_all=0         #响应总数
Num_query_success=0     #查询成功总数，不只有a aaaa
Num_query_fail=0        #查询失败总数

Num_query_a_all=0       #查询a记录总数
Num_query_a_success=0   #查询a记录成功数
Num_query_a_fail=0      #查询a记录失败数
Num_query_aaaa_all=0    #查询aaaa总数
Num_query_aaaa_success=0#查询aaaa成功数
Num_query_aaaa_fail=0   #查询aaaa失败数

Dic_record_num_all={}       #该种类的记录对应的查询数
Dic_record_num_success={}   #该种类的记录对应的查询成功数
#这个分析的不只是Rcode 0且非空了，是所有的响应！
#key为1 A 28 AAAA val为字典，字典key为对应数量、各个rcode数量（no error data/no error nodata/success/nxdomain/other error）、不同fqdn数量、sld数量、tld数量、pubsuf数量
Dic_type_dic={}             #所有响应中种类 对应的数量、占总量比例、各个rcode数量（输出时变为比例），qdots，fqdn、sld、tld、is pubsuf

####注意分nxdomain啥的 重新考虑
Dic_domain_num_a_all={}     #该域名a查询总数
Dic_domain_num_a_success={} #该域名a查询成功数
Dic_domain_num_a_fail={}    #该域名a查询失败数
Dic_domain_num_aaaa_all={}  #该域名aaaa查询总数
Dic_domain_num_aaaa_success={}#该域名aaaa查询成功数
Dic_domain_num_aaaa_fail={} #该域名aaaa查询失败数
Dic_domain_dic={}

Dic_resolver_num_all={}     #该解析器查询总数
Dic_resolver_num_success={} #该解析器查询成功数
Dic_resolver_num_fail={}    #该解析器查询失败数
Dic_resolver_num_a_all={}   #该解析器查询a记录总数
Dic_resolver_num_a_success={}#该解析器查询a记录成功数
Dic_resolver_num_a_fail={}  #该解析器查询a记录失败数
Dic_resolver_num_aaaa_all={}#该解析器查询aaaa记录总数
Dic_resolver_num_aaaa_success={}#该解析器查询aaaa记录成功数
Dic_resolver_num_aaaa_fail={}#该解析器查询aaaa记录的失败数
Dic_resolver_asnum={}       #该解析器对应的as号
Dic_asnum_asname={}         #该as号对应的as名
Dic_resolver_public_num_all={}#某公共解析器查询总数
Dic_resolver_public_num_success={}
Dic_resolver_public_num_a_all={}
Dic_resolver_public_num_a_success={}
Dic_resolver_public_num_aaaa_all={}
Dic_resolver_public_num_aaaa_success={}
Dic_ip_resolver={}
Dic_resolver_dic={}         #记录不同解析器返回的各种rcode

#NXDomain
Dic_nxdomain_num={} #nxdomain最多的fqdn
Dic_nxsld_num={}    #nxdomain最多的nxsld
Dic_nxclient_num={}     #nxdomain发起最多的client
Num_nxpubsuf=0

#不同用户发起查询数量
Dic_client_query_num={}
#不同用户发起查询造成的状态
Dic_client_Rstatus_dic={}
Dic_client_Qtype_dic={}
Dic_client_domain_dic={}