#统计ipv6数据集中 ptr and NXDomain中 查询私有ip域名的日志数量
import data
import pandas as pd
from tqdm import tqdm
import csv
from easy_fun import judge_priptr,fqdn2pubsuf
from main import init
init()
file_name='source_data_new/2023-08-30-DNS.csv'
#下面这个要对应准
fin=open(file_name,'r',encoding='utf-8')
csv_in=csv.reader(fin)
next(csv_in)
Dic_item={}
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
ii=0
# for item in data.List_pubsuf:
#     print(item)
#     ii+=1
#     if ii>10:
#         break
for line in tqdm(csv_in):
    i+=1
    # if i<4450000:
    #     continue
    # if i>1000000:
    #     break
    #这个顺序无所谓
    Client  =   line[24]#用户ip
    Resolver=   line[33]#解析器ip
    DiaID   =   line[112]#dns事务ID 判断有多少个会话
    QorR    =   line[113]#0是query 1是response
    Rcode   =   line[119]#响应状态0 No Error 3 NXDomain
    Qname   =   line[124].lower()
    Qtype   =   int(line[125])#该响应的查询种类 （数字类型
    Rjson   =   line[129]
    if QorR=='0':
        continue
    if Qtype==33:
        Dic_item['index'].append(i)
        Dic_item['unixtime'].append(line[0])
        Dic_item['DiaID'].append(DiaID)
        Dic_item['QorR'].append(QorR)
        Dic_item['Rcode'].append(Rcode)
        Dic_item['Qname'].append(Qname)
        Dic_item['Qtype'].append(Qtype)
        Dic_item['Client'].append(Client)
        Dic_item['Resolver'].append(Resolver)
        Dic_item['Rjson'].append(Rjson)
dfout=pd.DataFrame(Dic_item)
dfout_sorted=dfout.sort_values(by=['Rcode'])
print('sorting dataframe...')
dfout_sorted.to_csv('other_data/test_select_SRV.csv')