import redis
import os
import sys

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
mapping = {
    'cat'   : 'Patitas',
    'dog'   : 'Pirana',
    'turtle': 'Ninja'
}

r.hset( 'animals', mapping= mapping )

result = r.hgetall( 'animals' )
print( result )

# insert or update just one attribute in a hash
r.hset( 'animals', 'fish', 'Baby Shark'  )


print( 'delete turtle' )
r.hdel( 'animals', 'turtle' )

result = r.hgetall( 'animals' )
print( result )


# ------------------------------------------------------------

# ------------------------------------------------------------


print( '\n\n End \n' )

