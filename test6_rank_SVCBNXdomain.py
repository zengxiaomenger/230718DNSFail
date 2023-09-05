# 输出PTR记录的NXDomain的域名排名
from tqdm import tqdm
import csv
file_name='source_data_new/v6/DNS_COLLECT_LOG.csv'
#下面这个要对应准
fin=open(file_name,'r',encoding='utf-8')
csv_in=csv.reader(fin)
next(csv_in)
Dic_domain_num={}
lis_tp=[]
i=0
for line in tqdm(csv_in):
    i+=1
    # if i>100000:
    #     break
    if line[45]=='3' and line[46]=='12':#Rcode是3 Qtype是1
        Qname=line[48].lower()
        if 'in-addr.arpa' not in Qname and 'ip6.arpa' not in Qname:
            lis_tp.append(Qname)
        if Qname not in Dic_domain_num:
            Dic_domain_num[Qname]=1
        else:
            Dic_domain_num[Qname]+=1
Dic_domain_num_sorted=dict(sorted(Dic_domain_num.items(),key=lambda x:x[1],reverse=True))
fout=open('other_data/test6_rank_SVCBNXdomain.csv','w',encoding='utf-8',newline='')
csv_out=csv.writer(fout)
for key,val in Dic_domain_num_sorted.items():
    csv_out.writerow([key,val])
