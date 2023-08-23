#main.py
import data
import awdb
import idna
from function import process
from output import output
def _init_():
    #读asnum2asname
    fin=open('./other_data/asnum2asname.txt',encoding='utf-8')
    for line in fin:
        list_tp=line.split(None,1)
        data.Dic_asnum_asname[list_tp[0]]=list_tp[1].strip()
    fin.close()

    #读public suffix
    fin=open('./other_data/public_suffix.txt',encoding='utf-8')
    for line in fin:
        tp=''
        pubsuf=''
        
        if line.isspace():
            continue
        if line[0]=='/' and line[1]=='/':

            continue
        if line[0]=='*' and line[1]=='.':
            tp=line[2:]
        elif line[0]=='!':
            tp=line[1:]
        else:
            tp=line
        pubsuf=tp.strip()
        data.List_pubsuf.append(idna.encode(pubsuf).decode())

    #读country
    fin=open('./other_data/country.txt')
    for line in fin:
        country=line.strip()
        data.List_country.append(country)

    #读 new gTLDs
    fin=open('./other_data/new_gtlds_1686227471.csv',encoding='utf-8')
    for line in fin:
        tp=line.split(',',1)
        data.List_newgTLDs.append(tp[0].strip())
    fin.close()

if __name__=='__main__':
    _init_()
    process()
    output()