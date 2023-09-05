#统计ipv6数据集中 ptr and NXDomain中 查询私有ip域名的日志数量
import pandas as pd
from tqdm import tqdm
import csv
from easy_fun import judge_priptr,fqdn2pubsuf
file_name='source_data_new/v6/DNS_COLLECT_LOG.csv'
#下面这个要对应准
fin=open(file_name,'r',encoding='utf-8')
csv_in=csv.reader(fin)
Dic_item={}
cnt123=0
cnt123_pri=0
Dic_item['index']=[]
Dic_item['unixtime']=[]
Dic_item['DiaID']=[]
Dic_item['QorR']=[]
Dic_item['Rcode']=[]
Dic_item['Qname']=[]
Dic_item['Qtype']=[]
Dic_item['Client']=[]
Dic_item['Resolver']=[]
Dic_item['Rjson']=[]

i=0
for line in tqdm(csv_in):
    i+=1
    # if i<4450000:
    #     continue
    # if i>10000:
    #     break
    #这个顺序无所谓
    QorR=line[39]
    if QorR=='0':
        continue
    Qname=line[48].lower()
    Qtype=int(line[46])
    if Qtype!=12:
        continue
    Rcode=line[45]
    if Rcode!='3':
        continue
    cnt123+=1
    # if fqdn2pubsuf(Qname)!='null':
    #     continue
    if judge_priptr(Qname)==True:
        cnt123_pri+=1
        Dic_item['index'].append(i)
        Dic_item['unixtime'].append(line[2])
        Dic_item['DiaID'].append(line[34])
        Dic_item['QorR'].append(line[39])
        Dic_item['Rcode'].append(line[45])
        Dic_item['Qname'].append(line[48])
        Dic_item['Qtype'].append(line[46])
        Dic_item['Client'].append(line[11])
        Dic_item['Resolver'].append(line[16])
        Dic_item['Rjson'].append(line[49])
dfout=pd.DataFrame(Dic_item)
dfout_sorted=dfout.sort_values(by=['Rcode'])
print('sorting dataframe...')
dfout_sorted.to_csv('other_data/test6_select_PTRNXpri.csv')