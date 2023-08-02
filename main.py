#main.py
import data
from tqdm import tqdm
from function import process
from output import output0,output1,output2,public_resolver

def _init_():
    #读asnum2asname
    fin=open('./other_data/asnum2asname.txt',encoding='utf-8')
    i=0
    for line in fin:
        list_tp=line.split(None,1)
        data.Dic_asnum_asname[list_tp[0]]=list_tp[1].strip()
    fin.close()

    #读 new gTLDs
    fin=open('./other_data/new_gtlds_1686227471.csv',encoding='utf-8')
    i=0
    for line in fin:
        tp=line.split(',',1)
        data.List_newgTLDs.append(tp[0].strip())
    fin.close()

if __name__=='__main__':
    _init_()
    process()
    output0()
    output1()
    output2()
    public_resolver()