
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 22:06:34 2018

@author: Yanhong Simokat
"""

import pandas as pd
import warnings
warnings.filterwarnings("ignore")
#Part A

#1.	Load the file into a Pandas dataframe
zagat = pd.read_csv('zagats.txt',header=None,na_values='nan', names= ['line','rname','address','city','phone','cuisine'])

#2.	Extract the 'name' field from ‘line’ attribute. 
d1 = zagat['line'].str.extract(r'^([^\d]*)(\d.*)$', expand=True)
zagat['rname'],zagat['address'] = d1[0],d1[1]

#3. extract 'address','city','phone','cuisine'. As you extract, populate the data into zagat. 
d2 = zagat['address'].str.extract(r'(\d.*\.)(\W.*)(\d{3}\-\d{3}\-\d{4})(.*)', expand=True)

#check null balues
d3 = zagat.ix[d2.iloc[:,0].isnull()].index
#since there are null values
d4 = zagat['address'].str.extract(r'(\d.*(PCH|Way|Walk|Broadway|Plaza))(\W.*)(\d{3}\-\d{3}\-\d{4})(.*)', expand=True)
d5 = zagat['address'].str.extract(r'^(\d{3}\-\d{3}\-\d{4})(\W.*)', expand=True)

zagat['address'],zagat['city'],zagat['phone'],zagat['cuisine']=d2[0],d2[1],d2[2],d2[3]

a = d4.ix[d4.iloc[:,0].notnull()].index.values
a1 = []
for i in a:
    if i in d3:
        a1.append(i)
        
b = d5.ix[d5.iloc[:,0].notnull()].index.values
b1 = []
for i in b:
    if i in d3:
        b1.append(i)
        
   
#for row 150 and 176, this two are special case
#s = [['lower level','Central Park'],['New York City','West New York']]
for i in a1:
    zagat['address'][i],zagat['city'][i],zagat['phone'][i],zagat['cuisine'][i]=d4[0][i],d4[2][i],d4[3][i],d4[4][i]
   
for j in b1:
    zagat['address'][j],zagat['city'][j],zagat['phone'][j],zagat['cuisine'][j]='None','None',d5[0][j],d5[1][j]
 
#check null values again
#null = zagat.isnull().sum()

# Load fodors.txt 
fodors = pd.read_csv('fodors.txt',header=None,na_values='nan', names= ['line','rname','address','city','phone','cuisine'])

f1 = fodors['line'].str.extract(r'^([^\d]*)(\d.*)$', expand=True)
fodors['rname'],fodors['address'] = f1[0],f1[1]

f2 = fodors['address'].str.extract(r'(\d.*\.)(\W.*)(\d{3}\/\d{3}\-\d{4}|\d{3}\/\d{3}\-\w{4}|\d{3}\/ \d{3}\-\d{4}|\d{3}\/\d{3}\-\-\d{4})(.*)', expand=True)
f4 = fodors['address'].str.extract(r'(\d.*(Northpoint|Circle|Way|Center|Plaza|Road|Broadway|Park|Alley))(\W.*)(\d{3}\/\d{3}\-\d{4})(.*)', expand=True)
f6 = fodors['address'].str.extract(r'(\d{1})(.San.*)(\d{3}\/\d{3}\-\d{4})(.*)', expand=True)
f8 = fodors['address'].str.extract(r'^(\d{3}\/\d{3}\-\d{4})(\W.*)', expand=True)

f5 = fodors.ix[f4.iloc[:,0].notnull()].index
c5 = []
for i in f5:
    c5.append(i)
    
f7 = fodors.ix[f6.iloc[:,0].notnull()].index
c7 = []
for i in f7:
    c7.append(i)
    
f9 = fodors.ix[f8.iloc[:,0].notnull()].index
c9 = []
for i in f9:
    c9.append(i)
    
fodors['address'],fodors['city'],fodors['phone'],fodors['cuisine']=f2[0],f2[1],f2[2],f2[3]

for i in c5:
    fodors['address'][i],fodors['city'][i],fodors['phone'][i],fodors['cuisine'][i]=f4[0][i],f4[2][i],f4[3][i],f4[4][i]
    
for i in c7:
    fodors['address'][i],fodors['city'][i],fodors['phone'][i],fodors['cuisine'][i]=f6[0][i],f6[1][i],f6[2][i],f6[3][i]
    
for i in c9:
    fodors['address'][i],fodors['city'][i],fodors['phone'][i],fodors['cuisine'][i]='None','None',f8[0][i],f8[1]
    
#print(fodors.to_string())
#pretty print
#print(zagat.to_string())

import sqlite3
conn = sqlite3.connect("dsc450.db")
c = conn.cursor()

c.execute("drop table if exists Restaurants")
restaurant = '''create table Restaurants(rname varchar2(100),address varchar(80),city varchar(40),
                phone varchar(20),cuisine varchar(50),latitude varchar(40),longitude varchar(40))'''
c.execute(restaurant)

import json
from urllib.request import urlopen
url = 'http://facsrv.cs.depaul.edu/~tmalik1/teaching/dsc450/geocode.csv'
with urlopen(url) as f:
    s = f.read().decode('utf8').replace("}\n{","},{")
    js = json.loads("["+s+']')
    
output = open('errors.txt','w')
count=0

for i in range(len(zagat)):
    lat = js[i]['results'][0]['geometry']['location']['lat']
    lng = js[i]['results'][0]['geometry']['location']['lng']
    address = js[i]['results'][0]['formatted_address'].split(',')[0]
    
    values = (zagat['rname'][i],zagat['address'][i],zagat['city'][i],
                zagat['phone'][i],zagat['cuisine'][i],lat,lng)
    if address in zagat['address'][i].replace('.',''):
        c.execute('insert into Restaurants values(?,?,?,?,?,?,?);',values)
    else:
        output.write("%s;\n" % str(address)) 
        count += 1

output.close()
conn.commit()

#sql statement
q1 = c.execute('select city,cuisine,count(*) from restaurants group by city,cuisine;').fetchall()
q2 = c.execute('select avg(latitude),avg(longitude) from restaurants where cuisine=" American" and city=" San Francisco ";').fetchall()
conn.close()

#match the phone format
for i in range(len(fodors['phone'])):
    fodors['phone'][i] = fodors['phone'][i].replace('/','-')
    fodors['phone'][i] = fodors['phone'][i].replace('--','-')
    fodors['phone'][i] = fodors['phone'][i].replace(' ','')

match = open('matching.txt','w')    
for i in range(fodors.shape[0]):
    for j in range(zagat.shape[0]):
        if fodors['phone'][i] in zagat['phone'][j]:
            m1 = fodors['rname'][i] + ' ' + fodors['address'][i] + ' ' + fodors['city'][i] + ' ' + fodors['phone'][i] + ' ' + fodors['cuisine'][i]
            m2 = zagat['rname'][j] + ' '+ zagat['address'][j] + ' ' + zagat['city'][j] + ' ' + zagat['phone'][j] + ' ' + zagat['cuisine'][j]
            match.write("%s;\n" % str(m1))
            match.write("%s;\n" % str(m2))
            match.write('############################# \n')

