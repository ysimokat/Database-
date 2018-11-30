# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 23:08:29 2018

@author: Yanhong Simokat
"""

from sqlalchemy import create_engine
import pandas as pd
import json

import warnings
warnings.filterwarnings('ignore')

engine = create_engine('sqlite:///part1.db', echo=True)

from sqlalchemy import Table,Column, Integer, String, MetaData

metadata = MetaData()

tweet_table = Table('tweet', metadata, 
                      Column('created_at', String),
                      Column('id_str',Integer),
                      Column('text',String),
                      Column('source',String),
                      Column('in_reply_to_user_id',String),
                      Column('in_reply_to_screen_name',String),
                      Column('in_reply_to_status_id',String),
                      Column('retweet_count',Integer),
                      Column('contributors',String))
 

metadata.create_all(engine)

data = pd.read_csv('Tweet1_Assignment4.txt',delimiter='EndOfTweet',encoding='utf8',na_values = 'nan')

insert_stmt = tweet_table.insert(bind=engine)
compiled_stmt = insert_stmt.compile()
print(compiled_stmt.params)

for i in data:
    d = json.loads(i)
    insert_stmt.execute(d)
    
metadata.bind = engine 

from sqlalchemy import select
from sqlalchemy import func


#1.	Count the number of iPhone users and android users
q1 = select([func.count(tweet_table.c.source)]).where(tweet_table.c.source.like('%Android%') | (tweet_table.c.source.like('%iPhone%'))).execute().fetchall()
print(q1[0][0])

#2.	Count the number of tweets with users who are not replying
q2 = select([tweet_table.c.in_reply_to_user_id]).where(tweet_table.c.in_reply_to_user_id == None).execute().fetchall()
print(len(q2))












    

 
