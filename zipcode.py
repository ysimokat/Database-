#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 17:25:42 2018

@author: Yanhong Simokat
"""

import sqlite3
from sqlite3 import OperationalError
import pandas as pd
conn = sqlite3.connect("zipcode.db")
c = conn.cursor()

sql2 = '''create table if not exists RESTAURANT_LOCATIONS(
        rID int, name varchar2(100), 
        street_address varchar2(100), 
        city varchar(40), 
        state varchar(40), 
        zipcode number(10), 
        cuisine varchar2(100)
        )'''

c.execute("CREATE TABLE if not exists ZipCode(zip int,city text,state text,latitude text,longitude text,timezone text,dst int)")
c.execute(sql2)

#insert data into table ZipCode
d = pd.read_csv("CHIzipcode.csv",delimiter=',')
for i in range(len(d)):
    d1 = []
    for i in d.loc[i]:
        d1.append(str(i))
    #e = c.execute("insert into ZipCode values(?,?,?,?,?,?,?)",[i for i in d1])
    e = c.execute("insert into ZipCode values(?,?,?,?,?,?,?)",[i for i in d1])

e= c.execute('''select * from ZipCode''').fetchall()

with open('restaurant_loctions.sql','r') as h:
    s = h.read()
    s = s.split(';')
    for i in s:
        try:
            c.execute(i)
        except OperationalError, msg:
            print 'Error: ',msg
        
s = c.execute("select * from RESTAURANT_LOCATIONS").fetchall()

data = c.execute("select distinct b.name,b.zipcode,a.latitude,a.longitude from ZipCode a, RESTAURANT_LOCATIONS b where a.zip = b.zipcode").fetchall()
for i in data:
    name,zips,lat,longi = i
    print '{},{},"{}","{}"'.format(name,zips,round(float(lat),6),round(float(longi),5))

conn.commit()
conn.close()       