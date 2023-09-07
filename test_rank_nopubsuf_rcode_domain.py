# 输出PTR记录的NXDomain的域名排名
from tqdm import tqdm
import csv
from easy_fun import fqdn2pubsuf
from main import init
file_name='source_data_new/2023-08-30-DNS.csv'
#下面这个要对应准
init()
fin=open(file_name,'r',encoding='utf-8')
csv_in=csv.reader(fin)
next(csv_in)
Dic_domain0_num={}
Dic_domain3_num={}
i=0
for line in tqdm(csv_in):
    i+=1
    # if i>5000000:
    #     break
    Client  =   line[24]#用户ip
    Resolver=   line[33]#解析器ip
    DiaID   =   line[112]#dns事务ID 判断有多少个会话
    QorR    =   line[113]#0是query 1是response
    Rcode   =   line[119]#响应状态0 No Error 3 NXDomain
    Qname   =   line[124].lower()
    Qtype   =   int(line[125])#该响应的查询种类 （数字类型
    Rjson   =   line[129]
    if fqdn2pubsuf(Qname)=='null':
        if Rcode=='0':#Rcode是3 Qtype是1
            if Qname not in Dic_domain0_num:
                Dic_domain0_num[Qname]=1
            else:
                Dic_domain0_num[Qname]+=1
        elif Rcode=='3':#Rcode是3 Qtype是1
            if Qname not in Dic_domain3_num:
                Dic_domain3_num[Qname]=1
            else:
                Dic_domain3_num[Qname]+=1

Dic_domain_num_sorted=dict(sorted(Dic_domain0_num.items(),key=lambda x:x[1],reverse=True))
fout=open('other_data/test_rank_nopubsuf_rode0_domain.csv','w',encoding='utf-8',newline='')
csv_out=csv.writer(fout)
for key,val in Dic_domain_num_sorted.items():
    csv_out.writerow([key,val])

Dic_domain_num_sorted=dict(sorted(Dic_domain3_num.items(),key=lambda x:x[1],reverse=True))
fout=open('other_data/test_rank_nopubsuf_rode3_domain.csv','w',encoding='utf-8',newline='')
csv_out=csv.writer(fout)
for key,val in Dic_domain_num_sorted.items():
    csv_out.writerow([key,val])