#output.py
import os
import csv
import data
import pandas as pd
from easy_fun import *

def output0():#输出一些与数据集相关的东西
    file_name_dnsstatus='0_status.csv'
    file_out_path_dns_status=os.path.join(data.dir_out,file_name_dnsstatus)
    file_out_dns_status=open(file_out_path_dns_status,'w',encoding='utf-8',newline='')

    file_out_dns_status.write('Number of dir:\n')
    for k,v in data.Dic_dir.items():
        file_out_dns_status.write(str(k)+' '+str(v)+'\n')

    file_out_dns_status.write('Number of QorR:\n')
    file_out_dns_status.write(str(data.Num_query)+' '+str(data.Num_response)+'\n')

    file_out_dns_status.write('Rcode of DNS Responses:\n')
    Dic_state_sorted=dict(sorted(data.Dic_state.items(),key=lambda x:x[1],reverse=True))
    for key,val in Dic_state_sorted.items():
        file_out_dns_status.write(str(key)+' '+str(val)+'\n')
    
    file_out_dns_status.write('Number of manmade:\n')
    file_out_dns_status.write(str(data.Num_manmade)+'\n')

    file_out_dns_status.write('Number of new gTLDs:\n')
    file_out_dns_status.write(str(data.Num_newgTLDs)+'\n')
    
    file_out_dns_status.close()

def output1():#处理结果并输出
    file_name_type='1_type.csv'#存放不同类型查询数量、成功数量、失败数量、成功率
    file_out_path_type=os.path.join(data.dir_out,file_name_type)
    #不同记录类型输出
    Record_num_all_sorted=dict(sorted(data.Dic_record_num_all.items(),key=lambda x:x[1],reverse=True))
    file_out_type=open(file_out_path_type,'w',newline='')
    csv_out=csv.writer(file_out_type)
    csv_out.writerow(['type','num_all','rate_all','num_success','rate_success'])
    for key,val in Record_num_all_sorted.items():
        csv_out.writerow([key,val,numwith2(val/data.Num_query_all*100)+'%',\
                data.Dic_record_num_success[key],numwith2(data.Dic_record_num_success[key]/val*100)+'%'])
    
    #再输出另一个，不影响好伐
    file_name_type='1_type_status.csv'
    file_out_path_type=os.path.join(data.dir_out,file_name_type)
    #不同记录类型输出
    file_out_type=open(file_out_path_type,'w',newline='')
    csv_out=csv.writer(file_out_type)
    csv_out.writerow(['type','num_all','rate_all',\
                        #'num_success','rate_success',\#这一行因为所有响应有 但是dns fail响应里没有的type，所以不要了
                        'rate_no_error_data','rate_no_error_nodata','rate_nxdomain','rate_other_error',\
                        'num_avelen','num_fqdn','num_sld','num_tld','num_pubsuf'])
    Dic_type_dic_sorted=dict(sorted(data.Dic_type_dic.items(),key=lambda x:x[1]['num_all'],reverse=True))
    for key,val in Dic_type_dic_sorted.items():#按总量顺序排序
        csv_out.writerow([key,val['num_all'],numwith2(val['num_all']/data.Num_response*100)+'%',\
                #data.Dic_record_num_success[key],numwith2(data.Dic_record_num_success[key]/data.Dic_record_num_all[key]*100)+'%',\
                numwith2(val['num_no_error_data']/val['num_all']*100)+'%',\
                numwith2(val['num_no_error_nodata']/val['num_all']*100)+'%',\
                numwith2(val['num_nxdomain']/val['num_all']*100)+'%',\
                numwith2(val['num_other_error']/val['num_all']*100)+'%',\
                numwith2(val['num_qdots']/val['num_all']),\
                len(val['set_fqdn']),len(val['set_sld']),\
                len(val['set_tld']),val['num_pubsuf']])
    file_out_type.close()

def output2():
    #这是啥？？？？？？？
    data.Num_query_a_fail=data.Num_query_a_all-data.Num_query_a_success
    data.Num_query_aaaa_fail=data.Num_query_aaaa_all-data.Num_query_aaaa_success

    #不同域名a记录按失败次数高低输出
    file_name_domain_a='2_domain_a.csv'#存放域名与a记录相关
    file_out_path_domain_a=os.path.join(data.dir_out,file_name_domain_a)
    for key in data.Dic_domain_num_a_all:#a记录
        data.Dic_domain_num_a_fail[key]=data.Dic_domain_num_a_all[key]-data.Dic_domain_num_a_success[key]
    Dic_domain_num_a_fail_sorted=dict(sorted(data.Dic_domain_num_a_fail.items(),key=lambda x:x[1],reverse=True))
    file_out=open(file_out_path_domain_a,'w',newline='')
    csv_out=csv.writer(file_out)
    #domain域名，num_a_fail是这个域名a记录失败次数，rate_all是这个域名失败次数占所有a失败的次数
    #num_a_all是这个域名所有a记录查询的数量，num_a_success是这个域名所有a记录查询的成功数，rate_a_success是这个域名查询的成功率
    csv_out.writerow(['domain','num_a_fail','rate_all','num_a_all','num_a_success','rate_a_fail'])
    for key,val in Dic_domain_num_a_fail_sorted.items():
        csv_out.writerow([key,val,numwith2(val/data.Num_query_a_fail*100)+'%',\
                        data.Dic_domain_num_a_all[key],data.Dic_domain_num_a_success[key],\
                        numwith2(val/data.Dic_domain_num_a_all[key]*100)+'%'])

    #不同域名aaaa记录按失败次数高低输出
    file_name_domain_aaaa='2_domain_aaaa.csv'#存放域名与aaaa记录相关
    file_out_path_domain_aaaa=os.path.join(data.dir_out,file_name_domain_aaaa)
    for key in data.Dic_domain_num_aaaa_all:#aaaa记录
        data.Dic_domain_num_aaaa_fail[key]=data.Dic_domain_num_aaaa_all[key]-data.Dic_domain_num_aaaa_success[key]
    Dic_domain_num_aaaa_fail_sorted=dict(sorted(data.Dic_domain_num_aaaa_fail.items(),key=lambda x:x[1],reverse=True))
    file_out=open(file_out_path_domain_aaaa,'w',newline='')
    csv_out=csv.writer(file_out)
    #domain域名，num_aaaa_fail是这个域名a记录失败次数，rate_all是这个域名失败次数占所有a失败的次数
    #num_aaaa_all是这个域名所有a记录查询的数量，num_aaaa_success是这个域名所有a记录查询的成功数，rate_aaaa_success是这个域名查询的成功率
    csv_out.writerow(['domain','num_aaaa_fail','rate_all','num_aaaa_all','num_aaaa_success','rate_aaaa_fail'])
    for key,val in Dic_domain_num_aaaa_fail_sorted.items():
        csv_out.writerow([key,val,numwith2(val/data.Num_query_aaaa_fail*100)+'%',\
                        data.Dic_domain_num_aaaa_all[key],data.Dic_domain_num_aaaa_success[key],\
                        numwith2(val/data.Dic_domain_num_aaaa_all[key]*100)+'%'])
    
    #单独写个去低频的
    #不同域名a记录按失败次数高低输出
    Num_query_a_fail_frequent=0
    for key in data.Dic_domain_num_a_all:
        if data.Dic_domain_num_a_all[key]>=100:
            Num_query_a_fail_frequent+=data.Dic_domain_num_a_fail[key]
    for key in data.Dic_domain_num_a_all:#a记录
        data.Dic_domain_num_a_fail[key]=data.Dic_domain_num_a_all[key]-data.Dic_domain_num_a_success[key]
    Dic_domain_num_a_fail_sorted=dict(sorted(data.Dic_domain_num_a_fail.items(),key=lambda x:x[1],reverse=True))
    
    file_name_domain_a_frequent='2_domain_a_frequent.csv'#存放域名与a记录相关
    file_out_path_domain_a_frequent=os.path.join(data.dir_out,file_name_domain_a_frequent)
    file_out=open(file_out_path_domain_a_frequent,'w',newline='')
    csv_out=csv.writer(file_out)
    #domain域名，num_a_fail是这个域名a记录失败次数，rate_all是这个域名失败次数占所有a失败的次数
    #num_a_all是这个域名所有a记录查询的数量，num_a_success是这个域名所有a记录查询的成功数，rate_a_success是这个域名查询的成功率
    csv_out.writerow(['domain','num_a_fail','rate_all','num_a_all','num_a_success','rate_a_fail'])
    for key,val in Dic_domain_num_a_fail_sorted.items():
        if data.Dic_domain_num_a_all[key]>=100:
            if Num_query_a_fail_frequent==0:
                csv_out.writerow([key,val,'null',\
                                data.Dic_domain_num_a_all[key],data.Dic_domain_num_a_success[key],\
                                numwith2(val/data.Dic_domain_num_a_all[key]*100)+'%'])
            else:
                csv_out.writerow([key,val,numwith2(val/Num_query_a_fail_frequent*100)+'%',\
                                data.Dic_domain_num_a_all[key],data.Dic_domain_num_a_success[key],\
                                numwith2(val/data.Dic_domain_num_a_all[key]*100)+'%'])
    #不同域名aaaa记录按失败次数高低输出
    Num_query_aaaa_fail_frequent=0
    for key in data.Dic_domain_num_aaaa_all:
        if data.Dic_domain_num_aaaa_all[key]>=100:
            Num_query_aaaa_fail_frequent+=data.Dic_domain_num_aaaa_fail[key]
    for key in data.Dic_domain_num_aaaa_all:#aaaa记录
        data.Dic_domain_num_aaaa_fail[key]=data.Dic_domain_num_aaaa_all[key]-data.Dic_domain_num_aaaa_success[key]
    Dic_domain_num_aaaa_fail_sorted=dict(sorted(data.Dic_domain_num_aaaa_fail.items(),key=lambda x:x[1],reverse=True))

    file_name_domain_aaaa_frequent='2_domain_aaaa_frequent.csv'#存放域名与aaaa记录相关
    file_out_path_domain_aaaa_frequent=os.path.join(data.dir_out,file_name_domain_aaaa_frequent)
    file_out=open(file_out_path_domain_aaaa_frequent,'w',newline='')
    csv_out=csv.writer(file_out)
    #domain域名，num_aaaa_fail是这个域名a记录失败次数，rate_all是这个域名失败次数占所有a失败的次数
    #num_aaaa_all是这个域名所有a记录查询的数量，num_aaaa_success是这个域名所有a记录查询的成功数，rate_aaaa_success是这个域名查询的成功率
    csv_out.writerow(['domain','num_aaaa_fail','rate_all','num_aaaa_all','num_aaaa_success','rate_aaaa_fail'])
    for key,val in Dic_domain_num_aaaa_fail_sorted.items():
        if data.Dic_domain_num_aaaa_all[key]>=100:
            if Num_query_aaaa_fail_frequent==0:
                csv_out.writerow([key,val,'null',\
                                data.Dic_domain_num_aaaa_all[key],data.Dic_domain_num_aaaa_success[key],\
                                numwith2(val/data.Dic_domain_num_aaaa_all[key]*100)+'%'])
            else:
                csv_out.writerow([key,val,numwith2(val/Num_query_aaaa_fail_frequent*100)+'%',\
                                data.Dic_domain_num_aaaa_all[key],data.Dic_domain_num_aaaa_success[key],\
                                numwith2(val/data.Dic_domain_num_aaaa_all[key]*100)+'%'])
    #pubsuf相关
    file_name_pubsuf='2_domain_pubsuf_status.csv'
    file_out_path_pubsuf=os.path.join(data.dir_out,file_name_pubsuf)
    #不同记录类型输出
    file_out_pubsuf=open(file_out_path_pubsuf,'w',newline='')
    csv_out=csv.writer(file_out_pubsuf)
    csv_out.writerow(['ispubsuf','num_all','rate_all',\
                        'rate_no_error_data','rate_no_error_nodata','rate_nxdomain','rate_other_error',\
                        'num_avelen','num_fqdn','num_sld','num_tld'])
    Dic_domain_dic_sorted=dict(sorted(data.Dic_domain_dic.items(),key=lambda x:x[1]['num_all'],reverse=True))
    for key,val in Dic_domain_dic_sorted.items():#按总量顺序排序
        csv_out.writerow([key,val['num_all'],numwith2(val['num_all']/data.Num_response*100)+'%',\
                numwith2(val['num_no_error_data']/val['num_all']*100)+'%',\
                numwith2(val['num_no_error_nodata']/val['num_all']*100)+'%',\
                numwith2(val['num_nxdomain']/val['num_all']*100)+'%',\
                numwith2(val['num_other_error']/val['num_all']*100)+'%',\
                numwith2(val['num_qdots']/val['num_all']),\
                len(val['set_fqdn']),len(val['set_sld']),len(val['set_tld'])])
    file_out_pubsuf.close()

def output3():#输出公共解析器查询的相关情况
    #resolver所有查询输出
    file_name='3_resolver_all.csv'
    fout_path=os.path.join(data.dir_out,file_name)
    fout=open(fout_path,'w',newline='')
    csv_out=csv.writer(fout)
    csv_out.writerow(['resolver_ip','num_all','rate_all','num_success','rate_success','asnum','asname','country'])
    Dic_resolver_num_all_sorted=dict(sorted(data.Dic_resolver_num_all.items(),key=lambda x:x[1],reverse=True))
    for key,val in Dic_resolver_num_all_sorted.items():
        asnum=data.Dic_resolver_asnum[key]
        asname=''
        country=''
        if asnum=='null':
            asname='null'
            country='null'
        else:
            asnum='AS'+str(data.Dic_resolver_asnum[key])
            if asnum not in data.Dic_asnum_asname:
                asname='null'
                country='null'
            else:
                [asname,country]=data.Dic_asnum_asname[asnum].rsplit(', ',1)
        csv_out.writerow([key,val,numwith2(val/data.Num_query_all*100)+'%',\
                    data.Dic_resolver_num_success[key],\
                    numwith2(data.Dic_resolver_num_success[key]/val*100)+'%',\
                    asnum,asname,country])
        
    #resolver的a记录查询输出
    file_name='3_resolver_a.csv'
    fout_path=os.path.join(data.dir_out,file_name)
    fout=open(fout_path,'w',newline='')
    csv_out=csv.writer(fout)
    csv_out.writerow(['resolver_ip','num_a_all','rate_a_all','num_a_success','rate_a_success','asnum','asname','country'])
    Dic_resolver_num_a_all_sorted=dict(sorted(data.Dic_resolver_num_a_all.items(),key=lambda x:x[1],reverse=True))
    for key,val in Dic_resolver_num_a_all_sorted.items():
        asnum=data.Dic_resolver_asnum[key]
        asname=''
        country=''
        if asnum=='null':
            asname='null'
            country='null'
        else:
            [asname,country]=data.Dic_asnum_asname['AS'+str(data.Dic_resolver_asnum[key])].rsplit(', ',1)
        csv_out.writerow([key,val,numwith2(val/data.Num_query_a_all*100)+'%',\
                    data.Dic_resolver_num_a_success[key],\
                    numwith2(data.Dic_resolver_num_a_success[key]/val*100)+'%',\
                    asnum,asname,country])
    #resolver的aaaa记录查询输出
    file_name='3_resolver_aaaa.csv'
    fout_path=os.path.join(data.dir_out,file_name)
    fout=open(fout_path,'w',newline='')
    csv_out=csv.writer(fout)
    csv_out.writerow(['resolver_ip','num_aaaa_all','rate_aaaa_all','num_aaaa_success','rate_aaaa_success','asnum','asname','country'])
    Dic_resolver_num_aaaa_all_sorted=dict(sorted(data.Dic_resolver_num_aaaa_all.items(),key=lambda x:x[1],reverse=True))
    for key,val in Dic_resolver_num_aaaa_all_sorted.items():
        asnum=data.Dic_resolver_asnum[key]
        asname=''
        country=''
        if asnum=='null':
            asname='null'
            country='null'
        else:
            [asname,country]=data.Dic_asnum_asname['AS'+str(data.Dic_resolver_asnum[key])].rsplit(', ',1)
        csv_out.writerow([key,val,numwith2(val/data.Num_query_aaaa_all*100)+'%',\
                    data.Dic_resolver_num_aaaa_success[key],\
                    numwith2(data.Dic_resolver_num_aaaa_success[key]/val*100)+'%',\
                    asnum,asname,country])
    
    #读public_resolver list
    #重写公共解析器！！！！！！！！！！！！！！！！！！！！
    fin=open('./other_data/public_resolver_ip.txt')
    file_name='3_resolver_public.csv'
    fout_path=os.path.join(data.dir_out,file_name)
    fout=open(fout_path,'w',newline='')
    csv_out=csv.writer(fout)
    csv_out.writerow(['public_resolver','num_all','num_success','rate_success',\
                    'num_a_all','num_a_success','rate_a_success',\
                    'num_aaaa_all','num_aaaa_success','rate_aaaa_success'])
    for line in fin:#对于每个公共解析器
        [public_resolver,ips]=line.split(',',1)
        ips_list=ips.strip().split(',')#是个list
        public_resolver_num_all=0
        public_resolver_num_success=0
        public_resolver_num_a_all=0
        public_resolver_num_a_success=0
        public_resolver_num_aaaa_all=0
        public_resolver_num_aaaa_success=0
        for ip in ips_list:
            if ip in data.Dic_resolver_num_all:
                public_resolver_num_all+=data.Dic_resolver_num_all[ip]
            if ip in data.Dic_resolver_num_success:
                public_resolver_num_success+=data.Dic_resolver_num_success[ip]
            if ip in data.Dic_resolver_num_a_all:
                public_resolver_num_a_all+=data.Dic_resolver_num_a_all[ip]
            if ip in data.Dic_resolver_num_a_success:
                public_resolver_num_a_success+=data.Dic_resolver_num_a_success[ip]
            if ip in data.Dic_resolver_num_aaaa_all:
                public_resolver_num_aaaa_all+=data.Dic_resolver_num_aaaa_all[ip]
            if ip in data.Dic_resolver_num_aaaa_success:
                public_resolver_num_aaaa_success+=data.Dic_resolver_num_aaaa_success[ip]
        if public_resolver_num_all!=0:
            rate_success=numwith2(public_resolver_num_success/public_resolver_num_all*100)+'%'
        else:
            rate_success='null'
        if public_resolver_num_a_all!=0:
            rate_a_success=numwith2(public_resolver_num_a_success/public_resolver_num_a_all*100)+'%'
        else:
            rate_a_success='null'
        if public_resolver_num_aaaa_all!=0:
            rate_aaaa_success=numwith2(public_resolver_num_aaaa_success/public_resolver_num_aaaa_all*100)+'%'
        else:
            rate_aaaa_success='null'
        csv_out.writerow([public_resolver,public_resolver_num_all,public_resolver_num_success,rate_success,\
                        public_resolver_num_a_all,public_resolver_num_a_success,rate_a_success,\
                        public_resolver_num_aaaa_all,public_resolver_num_aaaa_success,rate_aaaa_success])

    file_name='3_status_resolver.csv'
    fout_path=os.path.join(data.dir_out,file_name)
    #不同记录类型输出
    fout=open(fout_path,'w',newline='')
    csv_out=csv.writer(fout)
    csv_out.writerow(['resolver','num_all','rate_all',\
                        'rate_no_error_data','rate_no_error_nodata','rate_nxdomain','rate_other_error'])
    Dic_resolver_dic_sorted=dict(sorted(data.Dic_resolver_dic.items(),key=lambda x:x[1]['num_all'],reverse=True))
    for key,val in Dic_resolver_dic_sorted.items():#按总量顺序排序
        csv_out.writerow([key,val['num_all'],numwith2(val['num_all']/data.Num_response*100)+'%',\
                numwith2(val['num_no_error_data']/val['num_all']*100)+'%',\
                numwith2(val['num_no_error_nodata']/val['num_all']*100)+'%',\
                numwith2(val['num_nxdomain']/val['num_all']*100)+'%',\
                numwith2(val['num_other_error']/val['num_all']*100)+'%'])
    #不同类型记录按公共解析器输出
    #重写公共解析器！！！！！！！！！！！！！！！！！！！！
    fin=open('./other_data/public_resolver_ip.txt')
    file_name='3_status_resolver_public.csv'
    fout_path=os.path.join(data.dir_out,file_name)
    fout=open(fout_path,'w',newline='')
    csv_out=csv.writer(fout)
    csv_out.writerow(['resolver','num_all','rate_all',\
                        'rate_no_error_data','rate_no_error_nodata','rate_nxdomain','rate_other_error'])
    for line in fin:#对于每个公共解析器
        [public_resolver,ips]=line.split(',',1)
        ips_list=ips.strip().split(',')#是个list
        public_resolver_num_all=0
        public_resolver_num_1=0
        public_resolver_num_2=0
        public_resolver_num_3=0
        public_resolver_num_4=0
        for ip in ips_list:
            if ip in data.Dic_resolver_dic:
                public_resolver_num_all+=data.Dic_resolver_dic[ip]['num_all']
                public_resolver_num_1+=data.Dic_resolver_dic[ip]['num_no_error_data']
                public_resolver_num_2+=data.Dic_resolver_dic[ip]['num_no_error_nodata']
                public_resolver_num_3+=data.Dic_resolver_dic[ip]['num_nxdomain']
                public_resolver_num_4+=data.Dic_resolver_dic[ip]['num_other_error']
        if public_resolver_num_all==0:
            csv_out.writerow([public_resolver,public_resolver_num_all,numwith2(public_resolver_num_all/data.Num_response*100)+'%',\
                          'null','null','null','null'])
        else:
            csv_out.writerow([public_resolver,public_resolver_num_all,numwith2(public_resolver_num_all/data.Num_response*100)+'%',\
                            numwith2(public_resolver_num_1/public_resolver_num_all*100)+'%',\
                            numwith2(public_resolver_num_2/public_resolver_num_all*100)+'%',\
                            numwith2(public_resolver_num_3/public_resolver_num_all*100)+'%',\
                            numwith2(public_resolver_num_4/public_resolver_num_all*100)+'%']) 

def output4():
    file_name_nxdomain_rank='4_nxdomain_rank.csv'
    file_out_path_nxdomain_rank=os.path.join(data.dir_out,file_name_nxdomain_rank)
    fout=open(file_out_path_nxdomain_rank,'w',encoding='utf-8',newline='')
    csv_out=csv.writer(fout)
    csv_out.writerow(['nxdomain','num'])

    Dic_nxdomain_num_sorted=dict(sorted(data.Dic_nxdomain_num.items(),key=lambda x:x[1],reverse=True))
    for k,v in Dic_nxdomain_num_sorted.items():
        csv_out.writerow([k,v])
    
    file_name_nxsld_rank='4_nxsld_rank.csv'
    file_out_path_nxsld_rank=os.path.join(data.dir_out,file_name_nxsld_rank)
    fout=open(file_out_path_nxsld_rank,'w',encoding='utf-8',newline='')
    csv_out=csv.writer(fout)
    csv_out.writerow(['nxsld','num'])
    Dic_nxsld_num_sorted=dict(sorted(data.Dic_nxsld_num.items(),key=lambda x:x[1],reverse=True))
    for k,v in Dic_nxsld_num_sorted.items():
        csv_out.writerow([k,v])
    fout.close()
    
    file_name_nxclient_rank='4_nxclient_rank.csv'
    file_out_path_nxclient_rank=os.path.join(data.dir_out,file_name_nxclient_rank)
    fout=open(file_out_path_nxclient_rank,'w',encoding='utf-8',newline='')
    csv_out=csv.writer(fout)
    csv_out.writerow(['nxclient','num'])
    Dic_nxclient_num_sorted=dict(sorted(data.Dic_nxclient_num.items(),key=lambda x:x[1],reverse=True))
    for k,v in Dic_nxclient_num_sorted.items():
        csv_out.writerow([k,v])
    fout.close()
    print('response的nxdomain中pubsuf数量：'+str(data.Num_nxpubsuf))
    print('response的nxdomain中非pubsuf总数量：'+str(data.Dic_state['3']-data.Num_nxpubsuf))
    print('response的nxdomain总数量：'+str(data.Dic_state['3']))

def output5():
    file_name_client_query_num='5_client_query_num.csv'
    file_name_client_Rstatus_dic='5_client_Rstatus_dic.csv'
    file_name_client_Qtype_dic='5_client_Qtype_dic.csv'
    file_name_client_domain_dic='5_client_domain_dic.csv'

    file_out_path_client_query_num=os.path.join (data.dir_out,   file_name_client_query_num)
    file_out_path_client_Rstatus_dic=os.path.join(data.dir_out,  file_name_client_Rstatus_dic)
    file_out_path_client_Qtype_dic=os.path.join (data.dir_out,   file_name_client_Qtype_dic)
    file_out_path_client_domain_dic=os.path.join(data.dir_out,   file_name_client_domain_dic)

    file_out=open(file_out_path_client_query_num,'w',encoding='utf-8',newline='')
    csv_out=csv.writer(file_out)
    Dic_client_query_num_sorted=dict(sorted(data.Dic_client_query_num.items(),key=lambda x:x[1],reverse=True))
    for key,val in Dic_client_query_num_sorted.items():
        csv_out.writerow([key,val])

    file_out=open(file_out_path_client_Rstatus_dic,'w',encoding='utf-8',newline='')
    csv_out=csv.writer(file_out)
    for key,val in Dic_client_query_num_sorted.items():
        csv_out.writerow([key,data.Dic_client_Rstatus_dic[key]])

    file_out=open(file_out_path_client_Qtype_dic,'w',encoding='utf-8',newline='')
    csv_out=csv.writer(file_out)
    for key,val in Dic_client_query_num_sorted.items():
        csv_out.writerow([key,data.Dic_client_Qtype_dic[key]])

    file_out=open(file_out_path_client_domain_dic,'w',encoding='utf-8',newline='')
    csv_out=csv.writer(file_out)
    for key,val in Dic_client_query_num_sorted.items():
        csv_out.writerow([key,data.Dic_client_domain_dic[key]])

def output6():
    #不同解析器处理的会话QR占比数量
    file_name='6_resolver_num_DialogQR.csv'
    fout_path=os.path.join(data.dir_out,file_name)
    fout=open(fout_path,'w',newline='')
    csv_out=csv.writer(fout)
    csv_out.writerow(['resolver','status'])
    Dic_resolver_QRdic_sorted=dict(sorted(data.Dic_resolver_QRdic.items(),key=lambda x:x[1]['all'],reverse=True))
    for key,val in Dic_resolver_QRdic_sorted.items():
        val_sorted=dict(sorted(val.items(),key=lambda x:x[1],reverse=True))
        csv_out.writerow([key,val_sorted])
    #统计 所有 解析器处理的会话QR占比数量
    data.Dic_resolver_all_QRdic={}
    data.Dic_resolver_all_QRdic['all']={}
    for key,val in data.Dic_resolver_QRdic.items():
        for k,v in val.items():
            if k not in data.Dic_resolver_all_QRdic['all']:
                data.Dic_resolver_all_QRdic['all'][k]=v
            else:
                data.Dic_resolver_all_QRdic['all'][k]+=v
    file_name='6_resolver_all_num_DialogQR.csv'
    fout_path=os.path.join(data.dir_out,file_name)
    fout=open(fout_path,'w',newline='')
    csv_out=csv.writer(fout)
    csv_out.writerow(['resolver','status'])
    for key,val in data.Dic_resolver_all_QRdic.items():
        val_sorted=dict(sorted(val.items(),key=lambda x:x[1],reverse=True))
        csv_out.writerow([key,val_sorted])
    file_name='6_resolver_all_rate_12.csv'
    fout_path=os.path.join(data.dir_out,file_name)
    fout=open(fout_path,'w',newline='')
    csv_out=csv.writer(fout)
    csv_out.writerow(['resolver','num_dialog','0_1','1_2','1_1','0_2','0_3','1_0','2_0','others'])
    for key,val in data.Dic_resolver_all_QRdic.items():
        for k in ['0_1','1_2','1_1','0_2','0_3','1_0','2_0']:
            if k not in val:
                val[k]=0
        csv_out.writerow([key,val['all'],\
                        numwith2(val['0_1']/val['all']*100)+'%',\
                        numwith2(val['1_2']/val['all']*100)+'%',\
                        numwith2(val['1_1']/val['all']*100)+'%',\
                        numwith2(val['0_2']/val['all']*100)+'%',\
                        numwith2(val['0_3']/val['all']*100)+'%',\
                        numwith2(val['1_0']/val['all']*100)+'%',\
                        numwith2(val['2_0']/val['all']*100)+'%',\
                        numwith2((val['all']-val['0_1']-val['1_2']-val['1_1']-val['0_2']\
                                    -val['0_3']-val['1_0']-val['2_0'])/val['all']*100)+'%'])
    #不同公共解析器处理的会话QR占比数量
    #先统计
    for key,val in Dic_resolver_QRdic_sorted.items():
        if judge_priIP(key)==True:
            key='10.0.0.0'
        #不考虑不是公共解析器的ip
        elif key not in data.Dic_ip_resolver:
            continue
        pubres=data.Dic_ip_resolver[key]
        if pubres not in data.Dic_resolver_public_QRdic:
            data.Dic_resolver_public_QRdic[pubres]=val
        else:
            for k,v in val.items():
                if k in data.Dic_resolver_public_QRdic[pubres]:
                    data.Dic_resolver_public_QRdic[pubres][k]+=v
                else:
                    data.Dic_resolver_public_QRdic[pubres][k]=v
    file_name='6_resolver_public_num_DialogQR.csv'
    fout_path=os.path.join(data.dir_out,file_name)
    fout=open(fout_path,'w',newline='')
    csv_out=csv.writer(fout)
    csv_out.writerow(['public_resolver','status'])
    Dic_resolver_public_QRdic_sorted=dict(sorted(data.Dic_resolver_public_QRdic.items(),key=lambda x:x[1]['all'],reverse=True))
    for key,val in Dic_resolver_public_QRdic_sorted.items():
        val_sorted=dict(sorted(val.items(),key=lambda x:x[1],reverse=True))
        csv_out.writerow([key,val_sorted])
    file_name='6_resolver_public_rate_12.csv'
    fout_path=os.path.join(data.dir_out,file_name)
    fout=open(fout_path,'w',newline='')
    csv_out=csv.writer(fout)
    csv_out.writerow(['public_resolver','num_dialog','0_1','1_2','1_1','0_2','0_3','1_0','2_0','others'])
    for key,val in Dic_resolver_public_QRdic_sorted.items():
        for k in ['0_1','1_2','1_1','0_2','0_3','1_0','2_0']:
            if k not in val:
                val[k]=0
        csv_out.writerow([key,val['all'],\
                        numwith2(val['0_1']/val['all']*100)+'%',\
                        numwith2(val['1_2']/val['all']*100)+'%',\
                        numwith2(val['1_1']/val['all']*100)+'%',\
                        numwith2(val['0_2']/val['all']*100)+'%',\
                        numwith2(val['0_3']/val['all']*100)+'%',\
                        numwith2(val['1_0']/val['all']*100)+'%',\
                        numwith2(val['2_0']/val['all']*100)+'%',\
                        numwith2((val['all']-val['0_1']-val['1_2']-val['1_1']-val['0_2']\
                                    -val['0_3']-val['1_0']-val['2_0'])/val['all']*100)+'%'])
    #下面输出0_1比较多的信息
    file_name='6_DialogQR01_Rcode.csv'
    fout_path=os.path.join(data.dir_out,file_name)
    fout=open(fout_path,'w',newline='',encoding='utf-8')
    csv_out=csv.writer(fout)
    csv_out.writerow(['Rcode','num'])
    Dic_DialogQR01_Rcode_sorted=dict(sorted(data.Dic_DialogQR01['Rcode'].items(),key=lambda x:x[1],reverse=True))
    for key,val in Dic_DialogQR01_Rcode_sorted.items():
        csv_out.writerow([key,val])

    file_name='6_DialogQR01_Client.csv'
    fout_path=os.path.join(data.dir_out,file_name)
    fout=open(fout_path,'w',newline='',encoding='utf-8')
    csv_out=csv.writer(fout)
    csv_out.writerow(['Client','num'])
    Dic_DialogQR01_Client_sorted=dict(sorted(data.Dic_DialogQR01['Client'].items(),key=lambda x:x[1],reverse=True))
    for key,val in Dic_DialogQR01_Client_sorted.items():
        csv_out.writerow([key,val])

    file_name='6_DialogQR01_Qname.csv'
    fout_path=os.path.join(data.dir_out,file_name)
    fout=open(fout_path,'w',newline='',encoding='utf-8')
    csv_out=csv.writer(fout)
    csv_out.writerow(['Qname','num'])
    Dic_DialogQR01_Qname_sorted=dict(sorted(data.Dic_DialogQR01['Qname'].items(),key=lambda x:x[1],reverse=True))
    for key,val in Dic_DialogQR01_Qname_sorted.items():
        csv_out.writerow([key,val])

    file_name='6_DialogQR01_Qtype.csv'
    fout_path=os.path.join(data.dir_out,file_name)
    fout=open(fout_path,'w',newline='',encoding='utf-8')
    csv_out=csv.writer(fout)
    csv_out.writerow(['Qtype','num'])
    Dic_DialogQR01_Qtype_sorted=dict(sorted(data.Dic_DialogQR01['Qtype'].items(),key=lambda x:x[1],reverse=True))
    for key,val in Dic_DialogQR01_Qtype_sorted.items():
        csv_out.writerow([key,val])

def output():
    output0()
    output1()
    output2()
    output3()
    output4()
    output5()
    # output6()