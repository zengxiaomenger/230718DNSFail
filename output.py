#output.py
import os
import csv
import data

def output0():#输出一些与数据集相关的东西
    dir_out='./result_data'
    file_name_dnsstatus='0_dns_status.csv'
    file_out_path_dns_status=os.path.join(dir_out,file_name_dnsstatus)
    file_out_dns_status=open(file_out_path_dns_status,'w',encoding='utf-8',newline='')
    
    file_out_dns_status.write('Number of dialog:\n')
    file_out_dns_status.write(str(data.Num_dialog)+'\n')

    file_out_dns_status.write('Number of dir:\n')
    for k,v in data.Dic_dir.items():
        file_out_dns_status.write(str(k)+' '+str(v)+'\n')

    file_out_dns_status.write('Number of QorR:\n')
    file_out_dns_status.write(str(data.Num_query)+' '+str(data.Num_response)+'\n')

    file_out_dns_status.write('Rcode of DNS Responses:\n')
    for key,val in data.Dic_state.items():
        file_out_dns_status.write(str(key)+' '+str(val)+'\n')
    
    file_out_dns_status.write('Number of manmade:\n')
    file_out_dns_status.write(str(data.Num_manmade)+'\n')

    file_out_dns_status.write('Number of new gTLDs:\n')
    file_out_dns_status.write(str(data.Num_newgTLDs)+'\n')
    
    file_out_dns_status.close()

def output1():#处理结果并输出
    dir_out='./result_data'
    file_name_type='1_type.csv'#存放不同类型查询数量、成功数量、失败数量、成功率
    file_out_path_type=os.path.join(dir_out,file_name_type)

    #不同记录类型输出
    Record_num_all_sorted=dict(sorted(data.Dic_record_num_all.items(),key=lambda x:x[1],reverse=True))
    file_out_type=open(file_out_path_type,'w',newline='')
    csv_out=csv.writer(file_out_type)
    csv_out.writerow(['type','num_all','rate_all','num_success','rate_success'])
    for key,val in Record_num_all_sorted.items():
        csv_out.writerow([key,val,str(format(val/data.Num_query_all*100,'.2f'))+'%',\
                data.Dic_record_num_success[key],str(format(data.Dic_record_num_success[key]/val*100,'.2f'))+'%'])

def output2():
    dir_out='./result_data'
    file_name_domain_a='2_domain_a.csv'#存放域名与a记录相关
    file_name_domain_aaaa='2_domain_aaaa.csv'#存放域名与aaaa记录相关
    file_out_path_domain_a=os.path.join(dir_out,file_name_domain_a)
    file_out_path_domain_aaaa=os.path.join(dir_out,file_name_domain_aaaa)
    data.Num_query_a_fail=data.Num_query_a_all-data.Num_query_a_success
    data.Num_query_aaaa_fail=data.Num_query_aaaa_all-data.Num_query_aaaa_success

    #不同域名a记录按失败次数高低输出
    for key in data.Dic_domain_num_a_all:#a记录
        data.Dic_domain_num_a_fail[key]=data.Dic_domain_num_a_all[key]-data.Dic_domain_num_a_success[key]
    Dic_domain_num_a_fail_sorted=dict(sorted(data.Dic_domain_num_a_fail.items(),key=lambda x:x[1],reverse=True))
    file_out_domain_a=open(file_out_path_domain_a,'w',newline='')
    csv_out=csv.writer(file_out_domain_a)
    #domain域名，num_a_fail是这个域名a记录失败次数，rate_all是这个域名失败次数占所有a失败的次数
    #num_a_all是这个域名所有a记录查询的数量，num_a_success是这个域名所有a记录查询的成功数，rate_a_success是这个域名查询的成功率
    csv_out.writerow(['domain','num_a_fail','rate_all','num_a_all','num_a_success','rate_a_fail'])
    for key,val in Dic_domain_num_a_fail_sorted.items():
        csv_out.writerow([key,val,str(format(val/data.Num_query_a_fail*100,'.2f'))+'%',\
                        data.Dic_domain_num_a_all[key],data.Dic_domain_num_a_success[key],\
                        str(format(val/data.Dic_domain_num_a_all[key]*100,'.2f'))+'%'])

    #不同域名aaaa记录按失败次数高低输出
    for key in data.Dic_domain_num_aaaa_all:#aaaa记录
        data.Dic_domain_num_aaaa_fail[key]=data.Dic_domain_num_aaaa_all[key]-data.Dic_domain_num_aaaa_success[key]
    Dic_domain_num_aaaa_fail_sorted=dict(sorted(data.Dic_domain_num_aaaa_fail.items(),key=lambda x:x[1],reverse=True))
    file_out_domain_aaaa=open(file_out_path_domain_aaaa,'w',newline='')
    csv_out=csv.writer(file_out_domain_aaaa)
    #domain域名，num_aaaa_fail是这个域名a记录失败次数，rate_all是这个域名失败次数占所有a失败的次数
    #num_aaaa_all是这个域名所有a记录查询的数量，num_aaaa_success是这个域名所有a记录查询的成功数，rate_aaaa_success是这个域名查询的成功率
    csv_out.writerow(['domain','num_aaaa_fail','rate_all','num_aaaa_all','num_aaaa_success','rate_aaaa_fail'])
    for key,val in Dic_domain_num_aaaa_fail_sorted.items():
        csv_out.writerow([key,val,str(format(val/data.Num_query_aaaa_fail*100,'.2f'))+'%',\
                        data.Dic_domain_num_aaaa_all[key],data.Dic_domain_num_aaaa_success[key],\
                        str(format(val/data.Dic_domain_num_aaaa_all[key]*100,'.2f'))+'%'])
    
    #单独写个去低频的
    #不同域名a记录按失败次数高低输出
    Num_query_a_fail_frequent=0
    for key in data.Dic_domain_num_a_all:
        if data.Dic_domain_num_a_all[key]>=100:
            Num_query_a_fail_frequent+=data.Dic_domain_num_a_fail[key]
    for key in data.Dic_domain_num_a_all:#a记录
        data.Dic_domain_num_a_fail[key]=data.Dic_domain_num_a_all[key]-data.Dic_domain_num_a_success[key]
    Dic_domain_num_a_fail_sorted=dict(sorted(data.Dic_domain_num_a_fail.items(),key=lambda x:x[1],reverse=True))
    file_out_domain_a=open('./result_data/2_domain_a_frequent.csv','w',newline='')
    csv_out=csv.writer(file_out_domain_a)
    #domain域名，num_a_fail是这个域名a记录失败次数，rate_all是这个域名失败次数占所有a失败的次数
    #num_a_all是这个域名所有a记录查询的数量，num_a_success是这个域名所有a记录查询的成功数，rate_a_success是这个域名查询的成功率
    csv_out.writerow(['domain','num_a_fail','rate_all','num_a_all','num_a_success','rate_a_fail'])
    for key,val in Dic_domain_num_a_fail_sorted.items():
        if data.Dic_domain_num_a_all[key]>=100:
            csv_out.writerow([key,val,str(format(val/Num_query_a_fail_frequent*100,'.2f'))+'%',\
                            data.Dic_domain_num_a_all[key],data.Dic_domain_num_a_success[key],\
                            str(format(val/data.Dic_domain_num_a_all[key]*100,'.2f'))+'%'])
    #不同域名aaaa记录按失败次数高低输出
    Num_query_aaaa_fail_frequent=0
    for key in data.Dic_domain_num_aaaa_all:
        if data.Dic_domain_num_aaaa_all[key]>=100:
            Num_query_aaaa_fail_frequent+=data.Dic_domain_num_aaaa_fail[key]
    for key in data.Dic_domain_num_aaaa_all:#aaaa记录
        data.Dic_domain_num_aaaa_fail[key]=data.Dic_domain_num_aaaa_all[key]-data.Dic_domain_num_aaaa_success[key]
    Dic_domain_num_aaaa_fail_sorted=dict(sorted(data.Dic_domain_num_aaaa_fail.items(),key=lambda x:x[1],reverse=True))
    file_out_domain_aaaa=open('./result_data/2_domain_aaaa_frequent.csv','w',newline='')
    csv_out=csv.writer(file_out_domain_aaaa)
    #domain域名，num_aaaa_fail是这个域名a记录失败次数，rate_all是这个域名失败次数占所有a失败的次数
    #num_aaaa_all是这个域名所有a记录查询的数量，num_aaaa_success是这个域名所有a记录查询的成功数，rate_aaaa_success是这个域名查询的成功率
    csv_out.writerow(['domain','num_aaaa_fail','rate_all','num_aaaa_all','num_aaaa_success','rate_aaaa_fail'])
    for key,val in Dic_domain_num_aaaa_fail_sorted.items():
        if data.Dic_domain_num_aaaa_all[key]>=100:
            csv_out.writerow([key,val,str(format(val/Num_query_aaaa_fail_frequent*100,'.2f'))+'%',\
                            data.Dic_domain_num_aaaa_all[key],data.Dic_domain_num_aaaa_success[key],\
                            str(format(val/data.Dic_domain_num_aaaa_all[key]*100,'.2f'))+'%'])

def output3():#输出公共解析器查询的相关情况
    dir_out='./result_data'
    file_name_resolver_all='3_resolver_all.csv'
    file_name_resolver_a='3_resolver_a.csv'
    file_name_resolver_aaaa='3_resolver_aaaa.csv'

    file_out_path_resolver_all=os.path.join(dir_out,file_name_resolver_all)
    file_out_path_resolver_a=os.path.join(dir_out,file_name_resolver_a)
    file_out_path_resolver_aaaa=os.path.join(dir_out,file_name_resolver_aaaa)

    #resolver所有查询输出
    Dic_resolver_num_all_sorted=dict(sorted(data.Dic_resolver_num_all.items(),key=lambda x:x[1],reverse=True))
    file_out_resolver_all=open(file_out_path_resolver_all,'w',newline='')
    csv_out=csv.writer(file_out_resolver_all)
    csv_out.writerow(['resolver_ip','num_all','rate_all','num_success','rate_success','asnum','asname','country'])
    for key,val in Dic_resolver_num_all_sorted.items():
        asnum=data.Dic_resolver_asnum[key]
        asname=''
        country=''
        if asnum=='null':
            asname='null'
            country='null'
        else:
            [asname,country]=data.Dic_asnum_asname['AS'+str(data.Dic_resolver_asnum[key])].rsplit(', ',1)
        csv_out.writerow([key,val,str(format(val/data.Num_query_all*100,'.2f'))+'%',\
                    data.Dic_resolver_num_success[key],\
                    str(format(data.Dic_resolver_num_success[key]/val*100,'.2f'))+'%',\
                    asnum,asname,country])
        
    #resolver的a记录查询输出
    Dic_resolver_num_a_all_sorted=dict(sorted(data.Dic_resolver_num_a_all.items(),key=lambda x:x[1],reverse=True))
    file_out_resolver_a=open(file_out_path_resolver_a,'w',newline='')
    csv_out=csv.writer(file_out_resolver_a)
    csv_out.writerow(['resolver_ip','num_a_all','rate_a_all','num_a_success','rate_a_success','asnum','asname','country'])
    for key,val in Dic_resolver_num_a_all_sorted.items():
        asnum=data.Dic_resolver_asnum[key]
        asname=''
        country=''
        if asnum=='null':
            asname='null'
            country='null'
        else:
            [asname,country]=data.Dic_asnum_asname['AS'+str(data.Dic_resolver_asnum[key])].rsplit(', ',1)
        csv_out.writerow([key,val,str(format(val/data.Num_query_a_all*100,'.2f'))+'%',\
                    data.Dic_resolver_num_a_success[key],\
                    str(format(data.Dic_resolver_num_a_success[key]/val*100,'.2f'))+'%',\
                    asnum,asname,country])
    #resolver的aaaa记录查询输出
    Dic_resolver_num_aaaa_all_sorted=dict(sorted(data.Dic_resolver_num_aaaa_all.items(),key=lambda x:x[1],reverse=True))
    file_out_resolver_aaaa=open(file_out_path_resolver_aaaa,'w',newline='')
    csv_out=csv.writer(file_out_resolver_aaaa)
    csv_out.writerow(['resolver_ip','num_aaaa_all','rate_aaaa_all','num_aaaa_success','rate_aaaa_success','asnum','asname','country'])
    for key,val in Dic_resolver_num_aaaa_all_sorted.items():
        asnum=data.Dic_resolver_asnum[key]
        asname=''
        country=''
        if asnum=='null':
            asname='null'
            country='null'
        else:
            [asname,country]=data.Dic_asnum_asname['AS'+str(data.Dic_resolver_asnum[key])].rsplit(', ',1)
        csv_out.writerow([key,val,str(format(val/data.Num_query_aaaa_all*100,'.2f'))+'%',\
                    data.Dic_resolver_num_aaaa_success[key],\
                    str(format(data.Dic_resolver_num_aaaa_success[key]/val*100,'.2f'))+'%',\
                    asnum,asname,country])
    
    #读public_resolver list
    fin=open('./other_data/public_resolver_ip.txt')
    fout=open('./result_data/3_resolver_public.csv','w',newline='')
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
            rate_success=str(format(public_resolver_num_success/public_resolver_num_all*100,'.2f'))+'%'
        else:
            rate_success='null'
        if public_resolver_num_a_all!=0:
            rate_a_success=str(format(public_resolver_num_a_success/public_resolver_num_a_all*100,'.2f'))+'%'
        else:
            rate_a_success='null'
        if public_resolver_num_aaaa_all!=0:
            rate_aaaa_success=str(format(public_resolver_num_aaaa_success/public_resolver_num_aaaa_all*100,'.2f'))+'%'
        else:
            rate_aaaa_success='null'
        csv_out.writerow([public_resolver,public_resolver_num_all,public_resolver_num_success,rate_success,\
                        public_resolver_num_a_all,public_resolver_num_a_success,rate_a_success,\
                        public_resolver_num_aaaa_all,public_resolver_num_aaaa_success,rate_aaaa_success])
    fin.close()
    fout.close()
def output4():
    Dic_nxdomain_num_sorted=dict(sorted(data.Dic_nxdomain_num.items(),key=lambda x:x[1],reverse=True))
    # print(Dic_nxdomain_num_sorted)
    fout=open('./result_data/4_nxdomain_rank.csv','w',encoding='utf-8',newline='')
    csv_out=csv.writer(fout)
    csv_out.writerow(['nxdomain','num'])
    for k,v in Dic_nxdomain_num_sorted.items():
        csv_out.writerow([k,v])
    
    Dic_nxsld_num_sorted=dict(sorted(data.Dic_nxsld_num.items(),key=lambda x:x[1],reverse=True))
    # print(Dic_nxsld_num_sorted)
    fout=open('./result_data/4_nxsld_rank.csv','w',encoding='utf-8',newline='')
    csv_out=csv.writer(fout)
    csv_out.writerow(['nxsld','num'])
    for k,v in Dic_nxsld_num_sorted.items():
        csv_out.writerow([k,v])
    fout.close()
    
    Dic_nxpubsuf_num_sorted=dict(sorted(data.Dic_nxpubsuf_num.items(),key=lambda x:x[1],reverse=True))
    # print(Dic_nxsld_num_sorted)
    fout=open('./result_data/4_nxpubsuf_rank.csv','w',encoding='utf-8',newline='')
    csv_out=csv.writer(fout)
    csv_out.writerow(['nxpubsuf','num'])
    for k,v in Dic_nxpubsuf_num_sorted.items():
        csv_out.writerow([k,v])
    fout.close()

def output5():
    dir_out='./result_data'
    file_name_client_query_num='5_client_query_num.csv'
    file_name_client_Rstatus_dic='5_client_Rstatus_dic.csv'
    file_name_client_Qtype_dic='5_client_Qtype_dic.csv'
    file_name_client_domain_dic='5_client_domain_dic.csv'

    file_out_path_client_query_num=os.path.join (dir_out,   file_name_client_query_num)
    file_out_path_client_Rstatus_dic=os.path.join(dir_out,  file_name_client_Rstatus_dic)
    file_out_path_client_Qtype_dic=os.path.join (dir_out,   file_name_client_Qtype_dic)
    file_out_path_client_domain_dic=os.path.join(dir_out,   file_name_client_domain_dic)

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

def output():
    output0()
    output1()
    output2()
    output3()
    output4()
    output5()