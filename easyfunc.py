import awdb
import data

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

def judge_success(Rdic_rr,Qname,Qtype):
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