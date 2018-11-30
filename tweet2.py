# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 14:38:15 2018

@author: Yanhong Simokat
"""

import json
import sqlite3

conn = sqlite3.connect("tweet.db")
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS TWEET")
c.execute("DROP TABLE IF EXISTS USER")

userTable = '''CREATE TABLE USER(
            ID INTEGER,
            NAME VARCHAR2(50),
            SCREEN_NAME VARCHAR2(50),
            DESCRIPTION VARCHAR2(100),
            FRIENDS_COUNT INTEGER,
            PRIMARY KEY (ID)
            );'''

tweetTable = '''CREATE TABLE TWEET(
            CREATED_AT VARCHAR2(35),
            ID_STR INTEGER,
            TEXT VARCHAR2(140),
            SOURCE VARCHAR2(100),
            IN_REPLY_TO_USER_ID VARCHAR2(50),
            IN_REPLY_TO_SCREEN_NAME VARCHAR2(50),
            IN_REPLY_TO_STATUS_ID VARCHAR2(50),
            RETWEET_COUNT INTEGER,
            CONTRIBUTORS VARCHAR2(100),
            USER_ID INTEGER,
            PRIMARY KEY (ID_STR),
            FOREIGN KEY (USER_ID) REFERENCES USER(ID)
            );'''

c.execute(userTable)
c.execute(tweetTable)

count = 0
output = open("Assignment4_errors.txt", "w")
f = open('Tweet2_Assignment4.txt',encoding='utf8')
print(f)
dic = {}
d = []  #going to store all the tweets in the list d
for tweet in f:
   
    try:    
        js = json.loads(tweet)
        
        uservalues = (js['user']['id'], js['user']['name'], js['user']['screen_name'], 
                      js['user']['description'], js['user']['friends_count'])
        
        tweetvalues = (js['created_at'], js['id_str'], js['text'], js['source'],
                       js['in_reply_to_user_id'], js['in_reply_to_screen_name'],
                       js['in_reply_to_status_id'], js['retweet_count'], js['contributors'], js['user']['id']) 
        c.execute("INSERT OR IGNORE INTO USER VALUES(?,?,?,?,?);",uservalues)
        c.execute("INSERT INTO TWEET VALUES(?,?,?,?,?,?,?,?,?,?);",tweetvalues)
        
        dic[js['user']['id'],js['user']['name']]=js['user']['friends_count']
        d.append(js['text'])
        
    except ValueError:
    # Handle the problematic tweet, which in your case would require writing it to another file
        output.write("%s;\n" % str(tweet.encode('utf8')))
            
    except Exception:       #for unique id constraint errors
        count = count + 1;
            
print(count)        #number of unique id constraint errors
output.close() 
f.close()

#Find the user(id,name) with the highest 'friend_count' in the databas
q1 = c.execute('SELECT ID,NAME FROM USER WHERE FRIENDS_COUNT = (SELECT MAX(FRIENDS_COUNT) FROM USER)').fetchall()
#print("The User with highest friend_count, ID:{}, Name:{} ".format(q1[0][0],q1[0][1]))

#Write Python code to find user with the highest 'friend_count'
for key, value in dic.items():
    if value == max(dic.values()):
        print("The User with highest friend_count, ID:{}, Name:{}".format(key[0],key[1]))

#find the tweets without associated user id entry
q2 = c.execute('select text from tweet').fetchall()
#print("tweets: ", q2)

#Write Python code to find the tweets
tweets = d
#print("tweets: ", tweets)

#Using Python, identify the top-3 most frequent terms in the text of the tweets.
terms={}
for i in tweets:
    words = i.strip().split(' ')
    for word in words:
        if word not in terms.keys():
            terms[word]=0
        terms[word] += 1
Keys = terms.keys()
Vals = terms.values()

# We could use dCount.items(), but we want the values to come first and the keys to be second
Pairs = zip(Vals, Keys)

s = sorted(Pairs, reverse=True)
#print('Top-3 most frequent terms: ', s[0],s[1],s[2])

    








conn.commit()
conn.close()