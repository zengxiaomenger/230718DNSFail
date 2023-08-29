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