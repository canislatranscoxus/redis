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

file_path = '/home/art/git/redis/maths/m1.lua'
with open( file_path, 'r' ) as f:
    text = f.read()
script = r.register_script( text )


r  = script( keys= [ 0 ], args = [ REDIS_DB  ] )
print( 'result: {}'.format( r ) )


