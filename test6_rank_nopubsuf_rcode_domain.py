# 输出PTR记录的NXDomain的域名排名
from tqdm import tqdm
import csv
from easy_fun import fqdn2pubsuf
from main import init
file_name='source_data_new/v6/DNS_COLLECT_LOG.csv'
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
    # if i>100000:
    #     break
    Qname=line[48].lower()
    Rcode=line[45]
    Qtype=line[46]
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
fout=open('other_data/test6_rank_nopubsuf_rode0_domain.csv','w',encoding='utf-8',newline='')
csv_out=csv.writer(fout)
for key,val in Dic_domain_num_sorted.items():
    csv_out.writerow([key,val])

Dic_domain_num_sorted=dict(sorted(Dic_domain3_num.items(),key=lambda x:x[1],reverse=True))
fout=open('other_data/test6_rank_nopubsuf_rode3_domain.csv','w',encoding='utf-8',newline='')
csv_out=csv.writer(fout)
for key,val in Dic_domain_num_sorted.items():
    csv_out.writerow([key,val])