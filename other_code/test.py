# fin=open('../230718DNSFail/source_data/DNSdata_1.csv','r',encoding='utf-8',newline='')
# lis=[]
# i=0
# for line in fin:
#     i+=1
#     if i>10000:
#         break
#     lis.append(line)
# fin.close()
# fout=open('../230718DNSFail/other_data/top10k.csv','w',encoding='utf-8',newline='')
# for line in lis:
#     fout.write(line)
# fout.close()
import idna
print(idna.encode('政府.com').decode())
print('//')