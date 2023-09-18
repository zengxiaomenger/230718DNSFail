import csv

fin1=open('result_data_new/2023-08-30-DNS/4_nxdomain_rank.csv','r')
fin2=open('result_data_new/2023-09-11-DNS/4_nxdomain_rank.csv','r',encoding='utf-8')

dic1={}
num1=0
num2=0
num=0
csv_in=csv.reader(fin1)
next(csv_in)
for line in csv_in:
    if line[1]=='':
        continue
    num1+=int(line[1])
    dic1[line[0]]=int(line[1])

csv_in=csv.reader(fin2)
next(csv_in)
for line in csv_in:
    if line[1]=='':
        continue
    num2+=int(line[1])
    if line[0] in dic1:
        num+=min(dic1[line[0]],int(line[1]))
print(num1)
print(num2)
print(num)
print(num/num1)
print(num/num2)