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
# import csv
# file_in_path='source_data_new/2023-08-24-DNS.csv'
# #输入的文件对象
# file_in=open(file_in_path,'r',encoding='utf-8-sig')
# csv_in=csv.reader(file_in)
# i=0
# tp0=0
# tp1=0
# tp2=0
# tp3=0
# for line in csv_in:#对于每一行数据!!!!!
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
import csv
file_in_path='source_data_new/2023-08-24-DNS.csv'
#输入的文件对象
file_in=open(file_in_path,'r',encoding='utf-8-sig')
csv_in=csv.reader(file_in)
i=0
Lis_time=[]
for line in csv_in:#对于每一行数据!!!!!
    i+=1
    time=line[0]
    if time<'1692860400':
        print('early than 3.')
        break
print('over')

# if '10'<'22':
#     print('yes')