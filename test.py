import os
from stat import S_IWRITE,S_IREAD
import random
import sys
import datetime
import csv
import pandas
from collections import deque
import shutil

try:
    j = "oo-oo"
    l = j.split('o')
except:
    print("BOO")
        

"""a = 'a,b,c,dd|ff|rr|jj,d1|f2|r3|j4,e,r'
b = a.split(',')
c1 = b[3]
c2 = b[4]

d1 = c1.split('|')
d2 = c2.split('|')

l1 = len(d1)

i = input()
k = 0
for j in d1:
    if j == i:
        d1.remove(j)
        d2.pop(k)
    k+=1

str1 = ''
count1 = 0
count2 = 0
str2 = ''
for i in d1:
    if count1 < l1-1:
        str1+=i
        count1+=1
        if count1 == l1-1:
            break
    str1 = str1+'|'

for j in d2:
    if count2 < l1-1:
        str2+=j
        count2+=1
        if count2 == l1-1:
            break
    str2 = str2+'|'

b[3] = str1
b[4] = str2
rec = ''
ct = 0
for i in b:
    rec = rec+i
    ct+=1
    if ct == len(b)-1:
        break
    rec = rec+','
    """
    
"""def makeRead():
    with open("text.txt",'a') as f:        
        f.write("Written now")
        
    os.chmod("text.txt",S_IREAD)
    main()

def makeWrite():
    with open("text.txt",'r') as f:    
        print(f.read())
        
    os.chmod("text.txt",S_IWRITE)
    main()
    
    
def main():  
    try:    
        a = int(input("What do you want to do?"))
        
        if a == 1:
            makeRead()
        else:
            makeWrite()
            
    except:
        print("Something wrong.")

if __name__ == "__main__":
    main()
## --------------------## 
a = 'bhootnath'
b = 'bhairavnath'
k = []
j = []
for i in range(len(a)):
    k.append(a[i])

for i in range(len(b)):
    j.append(b[i])

score = 0

if len(a) > len(b):
    print("In B")
    for i in range(len(b)):
        if b[i] in k:
            print(b[i])
            score+=1
        else:
            print(i,"-SKIP")
            continue
    
    print(round(score/len(b),4)*100,'%')
else:
    print("In A")
    for i in range(len(a)):
        if a[i] in j:
            print(a[i])
            score+=1
        else:
            print(i,"-SKIP")
            continue
    
    print(round(score/len(a),4)*100,'%')"""