# from tqdm import tqdm
# fin=open('source_data_new/v6/DNS_COLLECT_LOG.csv','r',encoding='utf-8',newline='')
# lis=[]
# i=0
# for line in tqdm(fin):
#     i+=1
#     if i<2950000:
#         continue
#     if i>2960000:
#         break
#     lis.append(line)
# fin.close()
# fout=open('other_data/source_top/DNS_COLLECT_LOG-top10k.csv','w',encoding='utf-8',newline='')
# for line in lis:
#     fout.write(line)
# fout.close()
# print(i)
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
#统计排序后事务id的数量
# import pandas as pd
# import data
# from output import *
# from dns_fun import dns_DialogQR
# from tqdm import tqdm

# if __name__=='__main__':
#     file_name=data.dir_in+'/2023-08-25-DNS.csv'
#     print('reading data......')
#     dfin=pd.read_csv(file_name,header=None,nrows=1000000)
#     print('read data over!')
#     Dic_item={}
#     Dic_item['index']=[]
#     Dic_item['DiaID']=[]
#     Dic_item['QorR']=[]
#     Dic_item['Rstatus']=[]
#     Dic_item['Qname']=[]
#     Dic_item['Qtype']=[]
#     Dic_item['Resolver']=[]
#     for index,line in tqdm(dfin.iterrows()):
#         Resolver=   line[33]
#         DiaID   =   line[112]
#         QorR    =   line[113]
#         Rstatus =   line[119]
#         Qname   =   line[124]
#         Qtype   =   line[125]
#         Dic_item['index'].append(index)
#         Dic_item['DiaID'].append(DiaID)
#         Dic_item['QorR'].append(QorR)
#         Dic_item['Rstatus'].append(Rstatus)
#         Dic_item['Qname'].append(Qname)
#         Dic_item['Qtype'].append(Qtype)
#         Dic_item['Resolver'].append(Resolver)
        
#     dfout=pd.DataFrame(Dic_item)
#     dfout_sorted=dfout.sort_values(by=['DiaID','index','Qname'])
#     dfout_sorted.to_csv('other_data/DialogID_sorted.csv')
#     num0=0
#     for index,line in dfout_sorted.iterrows():
#         num0+=1
#         dns_DialogQR(line['Qname'],line['QorR'],line['Resolver'])
#     print('num0:'+str(num0))
#     output31()
# import data
# import os
# import csv
# import json
# from main import init
# from easyfun import judge_priIP,numwith2
# init()
# fin=open('result_data_new/2023-08-25-DNS/3_resolver_num_DialogQR.csv','r',encoding='utf-8')
# csv_in=csv.reader(fin)
# next(csv_in)
# for line in csv_in:
#     json_str = line[1].replace("'", "\"")
#     data.Dic_resolver_QRdic[line[0]]=json.loads(json_str)
# #统计 所有 解析器处理的会话QR占比数量
# data.Dic_resolver_all_QRdic={}
# data.Dic_resolver_all_QRdic['all']={}
# for key,val in data.Dic_resolver_QRdic.items():
#     for k,v in val.items():
#         if k not in data.Dic_resolver_all_QRdic['all']:
#             data.Dic_resolver_all_QRdic['all'][k]=v
#         else:
#             data.Dic_resolver_all_QRdic['all'][k]+=v
# file_name='3_resolver_all_num_DialogQR.csv'
# fout_path=os.path.join(data.dir_out,file_name)
# fout=open(fout_path,'w',newline='')
# csv_out=csv.writer(fout)
# csv_out.writerow(['resolver','status'])
# for key,val in data.Dic_resolver_all_QRdic.items():
#     val_sorted=dict(sorted(val.items(),key=lambda x:x[1],reverse=True))
#     csv_out.writerow([key,val_sorted])
# file_name='3_resolver_all_rate_12.csv'
# fout_path=os.path.join(data.dir_out,file_name)
# fout=open(fout_path,'w',newline='')
# csv_out=csv.writer(fout)
# csv_out.writerow(['resolver','num_dialog','0_1','1_2','1_1','0_2','0_3','1_0','2_0','others'])
# for key,val in data.Dic_resolver_all_QRdic.items():
#     for k in ['0_1','1_2','1_1','0_2','0_3','1_0','2_0']:
#         if k not in val:
#             val[k]=0
#     csv_out.writerow([key,val['all'],\
#                       numwith2(val['0_1']/val['all']*100)+'%',\
#                       numwith2(val['1_2']/val['all']*100)+'%',\
#                       numwith2(val['1_1']/val['all']*100)+'%',\
#                       numwith2(val['0_2']/val['all']*100)+'%',\
#                       numwith2(val['0_3']/val['all']*100)+'%',\
#                       numwith2(val['1_0']/val['all']*100)+'%',\
#                       numwith2(val['2_0']/val['all']*100)+'%',\
#                       numwith2((val['all']-val['0_1']-val['1_2']-val['1_1']-val['0_2']\
#                                 -val['0_3']-val['1_0']-val['2_0'])/val['all']*100)+'%'])
# #不同公共解析器处理的会话QR占比数量
# #先统计
# for key,val in data.Dic_resolver_QRdic.items():
#     if judge_priIP(key)==True:
#         key='10.0.0.0'
#     #不考虑不是公共解析器的ip
#     elif key not in data.Dic_ip_resolver:
#         continue
#     pubres=data.Dic_ip_resolver[key]
#     if pubres not in data.Dic_resolver_public_QRdic:
#         data.Dic_resolver_public_QRdic[pubres]=val
#     else:
#         for k,v in val.items():
#             if k in data.Dic_resolver_public_QRdic[pubres]:
#                 data.Dic_resolver_public_QRdic[pubres][k]+=v
#             else:
#                 data.Dic_resolver_public_QRdic[pubres][k]=v
# file_name='3_resolver_public_num_DialogQR.csv'
# fout_path=os.path.join(data.dir_out,file_name)
# fout=open(fout_path,'w',newline='')
# csv_out=csv.writer(fout)
# csv_out.writerow(['public_resolver','status'])
# Dic_resolver_public_QRdic_sorted=dict(sorted(data.Dic_resolver_public_QRdic.items(),key=lambda x:x[1]['all'],reverse=True))
# for key,val in Dic_resolver_public_QRdic_sorted.items():
#     val_sorted=dict(sorted(val.items(),key=lambda x:x[1],reverse=True))
#     csv_out.writerow([key,val_sorted])
# file_name='3_resolver_public_rate_12.csv'
# fout_path=os.path.join(data.dir_out,file_name)
# fout=open(fout_path,'w',newline='')
# csv_out=csv.writer(fout)
# csv_out.writerow(['public_resolver','num_dialog','0_1','1_2','1_1','0_2','0_3','1_0','2_0','others'])
# for key,val in Dic_resolver_public_QRdic_sorted.items():
#     for k in ['0_1','1_2','1_1','0_2','0_3','1_0','2_0']:
#         if k not in val:
#             val[k]=0
#     csv_out.writerow([key,val['all'],\
#                       numwith2(val['0_1']/val['all']*100)+'%',\
#                       numwith2(val['1_2']/val['all']*100)+'%',\
#                       numwith2(val['1_1']/val['all']*100)+'%',\
#                       numwith2(val['0_2']/val['all']*100)+'%',\
#                       numwith2(val['0_3']/val['all']*100)+'%',\
#                       numwith2(val['1_0']/val['all']*100)+'%',\
#                       numwith2(val['2_0']/val['all']*100)+'%',\
#                       numwith2((val['all']-val['0_1']-val['1_2']-val['1_1']-val['0_2']\
#                                 -val['0_3']-val['1_0']-val['2_0'])/val['all']*100)+'%'])
# a=''
# b=''
# a='a' if False else b='b'
# print(a)

# str_0="[{DNS_RR_NAME=akamaiedge-staging.net, DNS_RR_TYPE=15, DNS_RR_CLASS=1, DNS_RR_TTL=600, DNS_RR_LENGTH=30, DNS_RR_MX=mx0a-00190b01.pphosted.com, DNS_RR_PREFERENCE=100, DNS_RR_CONTENT=mx0a-00190b01.pphosted.com,100}, {DNS_RR_NAME=akamaiedge-staging.net, DNS_RR_TYPE=15, DNS_RR_CLASS=1, DNS_RR_TTL=600, DNS_RR_LENGTH=18, DNS_RR_MX=mx0b-00190b01.pphosted.com, DNS_RR_PREFERENCE=100, DNS_RR_CONTENT=mx0b-00190b01.pphosted.com,100}, {DNS_RR_NAME=akamaiedge-staging.net, DNS_RR_TYPE=2, DNS_RR_CLASS=1, DNS_RR_TTL=90000, DNS_RR_LENGTH=21, DNS_RR_NS=a11-192.akamaiedge.net, DNS_RR_CONTENT=a11-192.akamaiedge.net}, {DNS_RR_NAME=akamaiedge-staging.net, DNS_RR_TYPE=2, DNS_RR_CLASS=1, DNS_RR_TTL=90000, DNS_RR_LENGTH=10, DNS_RR_NS=a13-192.akamaiedge.net, DNS_RR_CONTENT=a13-192.akamaiedge.net}, {DNS_RR_NAME=akamaiedge-staging.net, DNS_RR_TYPE=2, DNS_RR_CLASS=1, DNS_RR_TTL=90000, DNS_RR_LENGTH=10, DNS_RR_NS=ns6-194.akamaiedge.net, DNS_RR_CONTENT=ns6-194.akamaiedge.net}, {DNS_RR_NAME=akamaiedge-staging.net, DNS_RR_TYPE=2, DNS_RR_CLASS=1, DNS_RR_TTL=90000, DNS_RR_LENGTH=10, DNS_RR_NS=ns7-194.akamaiedge.net, DNS_RR_CONTENT=ns7-194.akamaiedge.net}, {DNS_RR_NAME=akamaiedge-staging.net, DNS_RR_TYPE=2, DNS_RR_CLASS=1, DNS_RR_TTL=90000, DNS_RR_LENGTH=9, DNS_RR_NS=a1-192.akamaiedge.net, DNS_RR_CONTENT=a1-192.akamaiedge.net}, {DNS_RR_NAME=akamaiedge-staging.net, DNS_RR_TYPE=2, DNS_RR_CLASS=1, DNS_RR_TTL=90000, DNS_RR_LENGTH=10, DNS_RR_NS=ns3-194.akamaiedge.net, DNS_RR_CONTENT=ns3-194.akamaiedge.net}, {DNS_RR_NAME=akamaiedge-staging.net, DNS_RR_TYPE=2, DNS_RR_CLASS=1, DNS_RR_TTL=90000, DNS_RR_LENGTH=9, DNS_RR_NS=a6-192.akamaiedge.net, DNS_RR_CONTENT=a6-192.akamaiedge.net}, {DNS_RR_NAME=akamaiedge-staging.net, DNS_RR_TYPE=2, DNS_RR_CLASS=1, DNS_RR_TTL=90000, DNS_RR_LENGTH=7, DNS_RR_NS=lar2.akamaiedge.net, DNS_RR_CONTENT=lar2.akamaiedge.net}, {DNS_RR_NAME=akamaiedge-staging.net, DNS_RR_TYPE=2, DNS_RR_CLASS=1, DNS_RR_TTL=90000, DNS_RR_LENGTH=10, DNS_RR_NS=ns5-194.akamaiedge.net, DNS_RR_CONTENT=ns5-194.akamaiedge.net}, {DNS_RR_NAME=akamaiedge-staging.net, DNS_RR_TYPE=2, DNS_RR_CLASS=1, DNS_RR_TTL=90000, DNS_RR_LENGTH=10, DNS_RR_NS=a28-192.akamaiedge.net, DNS_RR_CONTENT=a28-192.akamaiedge.net}, {DNS_RR_NAME=akamaiedge-staging.net, DNS_RR_TYPE=2, DNS_RR_CLASS=1, DNS_RR_TTL=90000, DNS_RR_LENGTH=6, DNS_RR_NS=la1.akamaiedge.net, DNS_RR_CONTENT=la1.akamaiedge.net}, {DNS_RR_NAME=akamaiedge-staging.net, DNS_RR_TYPE=2, DNS_RR_CLASS=1, DNS_RR_TTL=90000, DNS_RR_LENGTH=10, DNS_RR_NS=a12-192.akamaiedge.net, DNS_RR_CONTENT=a12-192.akamaiedge.net}, {DNS_RR_NAME=akamaiedge-staging.net, DNS_RR_TYPE=2, DNS_RR_CLASS=1, DNS_RR_TTL=90000, DNS_RR_LENGTH=6, DNS_RR_NS=la3.akamaiedge.net, DNS_RR_CONTENT=la3.akamaiedge.net}, {DNS_RR_NAME=akamaiedge-staging.net, DNS_RR_TYPE=16, DNS_RR_CLASS=1, DNS_RR_TTL=90000, DNS_RR_LENGTH=48, DNS_RR_TXT=Thisisnotthenameserveryouarelookingfor., DNS_RR_SIZE=47, DNS_RR_CONTENT=Thisisnotthenameserveryouarelookingfor.,47}, {DNS_RR_NAME=akamaiedge-staging.net, DNS_RR_TYPE=6, DNS_RR_CLASS=1, DNS_RR_TTL=90000, DNS_RR_LENGTH=51, DNS_RR_MNME=internal.akamaiedge.net, DNS_RR_RNAME=hostmaster.akamai.com, DNS_RR_SERIAL=1559044082, DNS_RR_REFRESH=90000, DNS_RR_RETRY=90000, DNS_RR_EXPIRE=90000, DNS_RR_MINIUM=180, DNS_RR_CONTENT=internal.akamaiedge.net,hostmaster.akamai.com,1559044082,90000,90000,90000,180}, {DNS_RR_NAME=, DNS_RR_TYPE=41, DNS_RR_UDP_PAYLOAD=4096, DNS_RR_RCODE=0, DNS_RR_VERSION=0, DNS_RR_Z=1, DNS_RR_LENGTH=0}]"
# #判断每个逗号前后的表达式都有等号
# pre=','
# #可以两个连续的等号，不能两个连续的逗号
# flag_ans=True#默认可以
# for c in str_0:
#     if c=='=':
#         if pre==',':
#             pre=c
#         elif pre=='=':
#             pre=c
#     elif c==',':
#         if pre==',':
#             flag_ans=False
#             break
#         elif pre=='=':
#             pre=c
# if flag_ans:
#     print('ok')
# else:
#     print('no')

# #这个是为了看看哪个是自己的ip
# import data
# import pandas as pd
# import csv
# from tqdm import tqdm
# file_name='other_data/check_log.csv'
# print('reading source data...')
# #下面这个要对应准
# dfin=pd.read_csv(file_name)
# Dic_Client_log={}
# for index,line in tqdm(dfin.iterrows()):
#     if line['Client'] not in Dic_Client_log:
#         Dic_Client_log[line['Client']]={}
#     if line['Resolver'] not in Dic_Client_log[line['Client']]:
#         Dic_Client_log[line['Client']][line['Resolver']]=0
#     Dic_Client_log[line['Client']][line['Resolver']]+=1
# dfout=pd.DataFrame(Dic_Client_log)
# # dfout.to_csv('other_data/check_log2.csv')
# fout=open('other_data/check_log2.csv','w',encoding='utf-8',newline='')
# csv_out=csv.writer(fout)
# for key,val in Dic_Client_log.items():
#     csv_out.writerow([key,val])

# import pandas as pd
# import csv
# from tqdm import tqdm
# file_name='other_data/check_log.csv'
# print('reading source data...')
# #下面这个要对应准
# dfin=pd.read_csv(file_name)
# dfout=dfin[dfin['Client']=='159.226.94.107'].sort_values(by=['unixtime'])
# dfout.to_csv('other_data/check_log3.csv')
# import os
# import csv
# from datetime import datetime

# def query_dns(resolver):
#     domain = "pan.baidu.com"
#     dns_server = resolver

#     # 构建dig命令
#     command = f"dig {domain} A @{dns_server}"
#     print(command)
#     # 执行命令并获取输出结果
#     result = os.popen(command).read()

#     # 获取当前时间
#     current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     # 写入CSV文件
#     # with open("dns_results.csv", "a", newline="") as csvfile:
#     #     writer = csv.writer(csvfile)
#     #     writer.writerow([current_time, domain, "A", dns_server, result])

# if __name__=='__main__':
#     resolver_list=['114.114.114.114','114.114.115.115',\
#                    '101.226.4.6','218.30.118.6',\
#                     '223.5.5.5','223.6.6.6',\
#                     '119.29.29.29','119.28.28.28',\
#                     '8.8.8.8','8.8.4.4',\
#                     '208.67.222.222','208.67.220.220',\
#                     '1.1.1.1','1.0.0.1',\
#                     '180.76.76.76',\
#                     '210.72.129.130','159.226.8.7',\
#                     '202.96.64.68','202.96.69.38',\
#                     '4.2.2.2','4.2.2.1',\
#                     '1.2.4.8','210.2.4.8',\
#                     '117.50.10.10','117.50.11.11'
#                 ]
#     for resolver in resolver_list:
#         query_dns(resolver)
#         # print(resolver)