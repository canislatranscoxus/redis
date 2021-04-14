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
                #,password = REDIS_AUTH
                ,decode_responses= True
                )

key = 'my_zset'

r.delete( key )


mapping = {
            'dog' : 5,
            'cat' : 1,
            'fish': 3
            }

r.zadd(key, mapping )

results = r.zrange(key, 0, -1)
print( results )

print( 'the elements in results are: \n' )
for i in results:
    print( i )

print( '\n\n End.' )    
