fin=open('./source_data/DNSdata_2.csv','r',encoding='utf-8',newline='')
lis=[]
i=0
for line in fin:
    i+=1
    if i>10000:
        break
    lis.append(line)
fin.close()
fout=open('./other_data/top10k.csv','w',encoding='utf-8',newline='')
for line in lis:
    fout.write(line)
fout.close()