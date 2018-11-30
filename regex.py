# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 13:33:14 2018

@author: Yanhong Simokat
"""

import re 

'''count the number of sections in this text.'''
d1 = open('Chicago.txt',encoding='utf8')
count = 0
for line in d1:
    pattern = '\[edit\]'
    if re.match(pattern,line):
        count+=1
print("the number of sections in this text: ", count)

'''In the Crime section, report all the years mentioned in sorted (ascending) order.'''
d1 = open('Chicago.txt',encoding='utf8')  
d = d1.read()
result = re.split('\[edit\]',d)

for i in result:
    line = i.strip().split()
    if line[0]=='Crime':
        index = i
index = index.strip().split()
y = []
for i in index:
    s = re.search('[0-9]{4}',i)
    if s:
        y.append(s.group())
print('All the years mentioned in Crime section: ',sorted(y))


'''Find all copunty names used in this file'''
d1 = open('Chicago.txt',encoding='utf8')
d = d1.read()
names=[]
result = re.split('\[edit\]',d)
for item in result:
    name1 = re.search('[A-Za-z][A-Za-z]+\sCounty',item)
    name2 = re.search('D[A-Za-z]+\sCounty',item)
    if name1 and name1.group() not in names:
        names.append(name1.group())
    if name2 and name2.group() not in names:
        names.append(name2.group())
print('County name used in Wikipedia Article: ',names)    

d1.close() #close the file