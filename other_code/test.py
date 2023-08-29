# fin=open('source_data_new/2023-08-25-DNS.csv','r',encoding='utf-8',newline='')
# lis=[]
# i=0
# for line in fin:
#     i+=1
#     if i>10000:
#         break
#     lis.append(line)
# fin.close()
# fout=open('other_data/2023-08-25-DNS-top10k.csv','w',encoding='utf-8',newline='')
# for line in lis:
#     fout.write(line)
# fout.close()
# import csv
# from tqdm import tqdm
# file_in_path='source_data_new/2023-06-12-DNS.csv'
# #输入的文件对象
# file_in=open(file_in_path,'r',encoding='utf-8-sig')
# csv_in=csv.reader(file_in)
# i=0
# tp0=0
# tp1=0
# tp2=0
# tp3=0
# for line in tqdm(csv_in):#对于每一行数据!!!!!
#     i+=1
#     if i>1000000:
#         break
#     QorR=line[113]
#     Rcode=line[119]
#     if QorR=='1':
#         if Rcode=='0':
#             tp0+=1
#         elif Rcode=='1':
#             tp1+=1
#         elif Rcode=='2':
#             tp2+=1
#         elif Rcode=='3':
#             tp3+=1
# print('i:'+str(i))
# print(tp0)
# print(tp1)
# print(tp2)
# print(tp3)
# import csv
# file_in_path='source_data_new/2023-08-24-DNS.csv'
# #输入的文件对象
# file_in=open(file_in_path,'r',encoding='utf-8-sig')
# csv_in=csv.reader(file_in)
# i=0
# Lis_time=[]
# for line in csv_in:#对于每一行数据!!!!!
#     i+=1
#     time=line[0]
#     if time<'1692860400':
#         print('early than 3.')
#         break
# print('over')

# # if '10'<'22':
# #     print('yes')
# Dic_ip_resolver={}
# import csv
# fin=open('other_data/public_resolver_ip.txt')
# fout=open('other_data/public_ip_resolver.txt','w',newline='')
# csv_out=csv.writer(fout)
# csv_out.writerow(['resolver','num_all','rate_all',\
#                     'rate_no_error_data','rate_no_error_nodata','rate_nxdomain','rate_other_error'])
# for line in fin:#对于每个公共解析器
#     [public_resolver,ips]=line.split(',',1)
#     ips_list=ips.strip().split(',')#是个list
#     for ip in ips_list:
#         Dic_ip_resolver[ip]=public_resolver
# print(Dic_ip_resolver)
import pandas as pd
from tqdm import tqdm
file_name='source_data_new/2023-08-25-DNS.csv'

print('reading data......')
dfin=pd.read_csv(file_name,header=None,nrows=1000000)
print('read data over!')

Dic_item={}
Dic_item['seq']=[]
Dic_item['DiaID']=[]
Dic_item['QorR']=[]
Dic_item['Rstatus']=[]
Dic_item['Qname']=[]
Dic_item['Qtype']=[]
i=0
for index,line in tqdm(dfin.iterrows()):
    i+=1
    DiaID   =   line[112]
    QorR    =   line[113]
    Rstatus =   line[119]
    Qname   =   line[124]
    Qtype   =   line[125]
    Dic_item['seq'].append(i)
    Dic_item['DiaID'].append(DiaID)
    Dic_item['QorR'].append(QorR)
    Dic_item['Rstatus'].append(Rstatus)
    Dic_item['Qname'].append(Qname)
    Dic_item['Qtype'].append(Qtype)
    
dfout=pd.DataFrame(Dic_item)

dfout.to_csv('other_data/DialogID_100k.csv')
dfout_sorted=dfout.sort_values(by=['DiaID','seq','Qname'])
dfout_sorted.to_csv('other_data/DialogID_100k_sorted.csv')