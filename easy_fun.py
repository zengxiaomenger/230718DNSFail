import awdb
import data
def fqdn2pubsuf(Qname):
    #如果是pubsuf，返回pubsuf，否则返回null
    pubsuf=Qname
    while True:
        if pubsuf in data.List_pubsuf:#这个后缀在公共后缀里
            break
        else:#当前后缀不在公共后缀里
            if len(pubsuf.split('.'))==1:#当前后缀长度为1
                pubsuf='null'
                break
            pubsuf=pubsuf.split('.',1)[1]
    return pubsuf
def judge_priptr(Qname):
    if 'home.arpa' in Qname:
        return True
    if 'in-addr.arpa' in Qname:
        lis_tp=Qname.split('.')
        if len(lis_tp)<6:
            return False
        ip=lis_tp[3]+'.'+lis_tp[2]+'.'+lis_tp[1]+'.'+lis_tp[0]
        if judge_priIP(ip)==True:
            return True
        else:
            return False
    if 'ip6.arpa' in Qname:
        #fec
        lis_tp=Qname.split('.')
        if len(lis_tp)<34:
            return False
        if lis_tp[-5]=='c' and lis_tp[-4]=='e' and lis_tp[-3]=='f' and lis_tp[-2]=='ip6' and lis_tp[-1]=='arpa':
            return True
        else:
            return False

def judge_recursive(Rdic_rr,Rname,Qname):
    if Rname==Qname:
        return 1
    else:
        tp=0
        for Ritem in Rdic_rr:
            if Ritem['type']==5 and Ritem['cname']==Rname:
                tp=judge_recursive(Rdic_rr,Ritem['name'],Qname)
                if tp==1:
                    break
        return tp

def judge_success(Rdic_rr,Qname,Qtype):#判断dns fail
    #复杂的判别方法是正着找，我们反着找！
    success=0
    for Ritem in Rdic_rr:#对于所有的答案
        if Ritem['type']==Qtype:
            if judge_recursive(Rdic_rr,Ritem['name'],Qname)==1:
                success=1
                break
        if success==1:
            break
    return success

def judge_recursive6(Rdic_rr,Rname,Qname):
    if Rname==Qname:
        return 1
    else:
        tp=0
        for Ritem in Rdic_rr:
            if int(Ritem['DNS_RR_TYPE'])==5 and Ritem['DNS_RR_CNAME']==Rname:
                tp=judge_recursive6(Rdic_rr,Ritem['DNS_RR_NAME'],Qname)
                if tp==1:
                    break
        return tp

def judge_success6(Rdic_rr,Qname,Qtype):
    #复杂的判别方法是正着找，我们反着找！
    success=0
    if Qtype!=1 and Qtype!=28:#不可能出现递归
        for Ritem in Rdic_rr:#直接找
            if Ritem['DNS_RR_NAME']==Qname and int(Ritem['DNS_RR_TYPE'])==Qtype:
                success=1
    else: #是1或28
        for Ritem in Rdic_rr:#对于所有的答案
            if int(Ritem['DNS_RR_TYPE'])==Qtype:
                if judge_recursive6(Rdic_rr,Ritem['DNS_RR_NAME'],Qname)==1:
                    success=1
                    break
            if success==1:
                break
    return success

def judge_priIP(ip):
    ip_sep4=ip.split('.')
    if ip_sep4[0]=='10':
        return True
    elif ip_sep4[0]=='192' and ip_sep4[1]=='168':
        return True
    elif ip_sep4[0]=='172' and int(ip_sep4[1])>=16 and int(ip_sep4[1])<=31:
        return True
    return False

def ip2asnum(str_ip):
    reader=awdb.open_database(r'./other_data/IP_basic_single_WGS84.awdb')
    (record,prefix_len)=reader.get_with_prefix_len(str_ip)
    ans=record.get('asnumber').decode('utf8')
    if ans!='':
        return ans
    else:
        return 'null'
def ip2asnum6(str_ip):#ipv6
    reader=awdb.open_database(r'./other_data/IP_city_single_BD09_WGS84_ipv6.awdb')
    (record,prefix_len)=reader.get_with_prefix_len(str_ip)
    ans=record.get('asnumber').decode('utf8')
    if ans!='':
        return ans
    else:
        return 'null'    

def fqdn2sld(fqdn):
    #www.baidu.com  www.baidu.com.cn
    #sld指sld+tld，如baidu.com
    tp=fqdn.split('.')
    ans=''
    #默认至少有三个
    if len(tp)>=3:
        if tp[-1] in data.List_country:
            ans=tp[-3]+'.'+tp[-2]+'.'+tp[-1]
        else:
            ans=tp[-2]+'.'+tp[-1]
    else:
        ans=fqdn
    return ans

def fqdn2tld(fqdn):
    tp=fqdn.split('.')
    return tp[-1]

def fqdn2qdots(fqdn):
    return len(fqdn.split('.'))

def numwith2(numdivnum):#把传来的相除变成两位小数
    return str(format(numdivnum,'.2f'))
def judge_json(str_0):#判断能否转为json
    pre=','
    #可以两个连续的等号，不能两个连续的逗号
    flag_ans=True#默认可以
    for c in str_0:
        if c=='=':
            if pre==',':
                pre=c
        elif c==',':
            if pre==',':
                flag_ans=False
                break
            elif pre=='=':
                pre=c
        elif c=='}':
            if pre==',':
                flag_ans=False
                break
    return flag_ans
##v6 rr响应转正常json
def str2json1(str_0):#这个快点，但是有些DNS_TXT不大合适
    #[{DNS_RR_NAME=smartont.net, DNS_RR_TYPE=6, DNS_RR_CLASS=1, DNS_RR_TTL=372, DNS_RR_LENGTH=52, DNS_RR_MNME=dns15.hichina.com, DNS_RR_RNAME=hostmaster.hichina.com, DNS_RR_SERIAL=2022052002, DNS_RR_REFRESH=3600, DNS_RR_RETRY=1200, DNS_RR_EXPIRE=86400, DNS_RR_MINIUM=600, DNS_RR_CONTENT=dns15.hichina.com,hostmaster.hichina.com,2022052002,3600,1200,86400,600}]
    str_1=str_0.replace(', ','\",\"')#  ,换成 ","
    str_2=str_1.replace('=','\":\"')# =换成":"
    str_3=str_2.replace('}\",\"{','\"},{\"')#}", "{换成"},{"
    str_4=str_3.replace('[{','[{\"')
    str_5=str_4.replace('}]','\"}]')
    return '{\"rr\":'+str_5+'}'
def str2json2(str0):#这个慢点，适配普遍
    #[{DNS_RR_NAME=push.apple.com, DNS_RR_TYPE=16, DNS_RR_CLASS=1, DNS_RR_TTL=2324, DNS_RR_LENGTH=9, DNS_RR_TXT=count=50china.com, DNS_RR_SIZE=8, DNS_RR_CONTENT=count=50china.com,8}]
    str1="{\"rr\":"
    i=-1
    flag_1=1#是否是逗号后的第一个等号
    for c in str0:
        i=i+1
        if i==0:
            str1+=c
        elif c=='{':
            str1+=(c+"\"")
        elif c=='=':
            if flag_1==1:#是逗号后的第一个等号
                str1+="\":\""#重要！！！！！
                flag_1=0
            else:
                str1+=c
        elif c==',':
            if str0[i+1]==' ':
                if str0[i-1]!='}':
                    str1+="\", \""
                else:
                    str1+=', '
                flag_1=1
            else:
                str1+=c
        elif c==' ':
            continue
        elif c=='}':
            str1+=("\""+c)
        elif i==len(str0)-1:
            str1+=c
        else:
            str1+=c
    str1+='}'
    return str1
