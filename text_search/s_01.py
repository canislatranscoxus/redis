'''
description: We connect to a redis enterprise Cloud instance from Redis Labs.
             The database instance has rediSearch module.
             And we insert documents, then make full text search.

about the libraries.
redis-py can connect, insert get hashes objects (dictionaries), 
but can not execute text search.

redisearch-py is the client that connect to redis and use the redisearch module 
to run the search queries.

--------------------------------------------------------

The Index was created using the next redis commands:

> FT.CREATE database_idx PREFIX 1 "doc:" 
SCORE 0.5 SCORE_FIELD "doc_score" 
SCHEMA 
title  TEXT 
body   TEXT 
url    TEXT 
visits NUMERIC


Insert data

> HSET doc:1 
title  "Redis Labs" body "Primary and caching" 
url    "<https://redislabs.com/primary-caching>" 
visits 108
'''

import redis
import os
import sys
from   redisearch import Client, TextField, IndexDefinition, Query


REDIS_HOST = os.environ[ 'REDIS_HOST' ]
REDIS_PORT = os.environ[ 'REDIS_PORT' ]
#REDIS_DB   = os.environ[ 'REDIS_DB'   ]
REDIS_DB   = 0
REDIS_AUTH = os.environ[ 'REDIS_AUTH' ]


# connect to redis
r = redis.Redis( host     = REDIS_HOST
                ,port     = REDIS_PORT
                ,db       = REDIS_DB
                ,password = REDIS_AUTH
                ,decode_responses= True
                )

# Insert key values in redis
r.set( 'animal:eagle', 'fly'  )

for i in range( 1, 7):
    r.delete( f'doc:{i}' )

key = 'doc:1'
r.hset( key, 'title' , 'Redis Labs')
r.hset( key, 'body'  , 'Primary and caching')
r.hset( key, 'url'   , '<https://redislabs.com/primary-caching>')
r.hset( key, 'visits', 108)

key = 'doc:2'
r.hset( key, 'title' , 'Redis Labs')
r.hset( key, 'body'  , 'Modules' )
r.hset( key, 'url'   , '<https://redislabs.com/modules>' )
r.hset( key, 'visits', 102 )
r.hset( key, 'doc_score', 0.8)

key = 'doc:3'
r.hset( key, 'title' , 'sharks attack in blue sea' )
r.hset( key, 'body'  , 'sharks ocean adventure' )
r.hset( key, 'url'   , '<https://sharks_attack.com/super-adventure>' )
r.hset( key, 'visits', '99' )


key = 'doc:4'
r.hset( key, 'title' , 'run for your life')
r.hset( key, 'body'  , 'The predators are running behind you, can you run faster?')
r.hset( key, 'url'   , 'www.runforyourlife.com')
r.hset( key, 'visits', '400')

key = 'doc:5'
r.hset( key, 'title' , 'skatebording goes wild')
r.hset( key, 'body'  , 'You will learn the best skateboard tricks.')
r.hset( key, 'url'   , 'www.sk8.com')
r.hset( key, 'visits', '500')

key = 'doc:6'
r.hset( key, 'title' , 'Pirate adventures')
r.hset( key, 'body'  , 'do you dare to fight other pirates and live many adventures to get the golden chest')
r.hset( key, 'url'   , 'www.piratelife.com')
r.hset( key, 'visits', '600')

# ------------------------------------------------------------
# Full text Search with rediSearch module.
# ------------------------------------------------------------


client = Client( index_name = 'database_idx'
, host= REDIS_HOST
, port= REDIS_PORT
, conn= r
, password = REDIS_AUTH  )

# Simple search
res = client.search( "adventures" )

# the result has the total number of results, and a list of documents


print( '\n Number of found docs: {}'.format( res.total ) ) # "2"
for d in res.docs:
    print( '{}. title: {}, body: {}'.format( d.id, d.title, d.body )   ) # "RediSearch"

print( '\n\n End \n' )

