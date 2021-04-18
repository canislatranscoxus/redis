import redis
import os
import sys

REDIS_HOST = os.environ[ 'REDIS_HOST' ]
REDIS_PORT = os.environ[ 'REDIS_PORT' ]
#REDIS_DB   = os.environ[ 'REDIS_DB'   ]
REDIS_DB   = 10
REDIS_AUTH = os.environ[ 'REDIS_AUTH' ]


# connect to redis
r = redis.Redis( host     = REDIS_HOST
                ,port     = REDIS_PORT
                ,db       = REDIS_DB
                ,password = REDIS_AUTH
                ,decode_responses= True
                )

file_path = '/home/art/git/redis/strings/strings.lua'
with open( file_path, 'r' ) as f:
    text = f.read()
script = r.register_script( text )


pattern = 'search_box:tf:*'
k1 = 'search_box:tf:eagle'
k2 = 'search_box:tf:mangost'
r  = script( keys= [ k1, k2 ], args = [ REDIS_DB, pattern ] )
print( 'result: {}'.format( r ) )
