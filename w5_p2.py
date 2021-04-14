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

def insert(minute_of_day: int, element: str):
    r.zadd(key, mapping={ element: minute_of_day } )


insert(0, "A")
insert(1, "B")
insert(2, "C")
insert(3, "A")

results = r.zrange(key, 0, -1)
print( results )

print( 'the elements in results are: \n' )
for i in results:
    print( i )

print( '\n\n End.' )    
