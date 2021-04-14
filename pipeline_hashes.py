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

r.hset( 'pet:1', 'id'    , '1'       )
r.hset( 'pet:1', 'animal', 'cat'     )
r.hset( 'pet:1', 'name'  , 'patitas' )
r.hset( 'pet:1', 'weapon', 'claws'   )

r.hset( 'pet:2', 'id'    , '2'       )
r.hset( 'pet:2', 'animal', 'dog'     )
r.hset( 'pet:2', 'name'  , 'spike'   )
r.hset( 'pet:2', 'weapon', 'fangs'   )

r.hset( 'pet:3', 'id'    , '3'       )
r.hset( 'pet:3', 'animal', 'snake'   )
r.hset( 'pet:3', 'name'  , 'squeeze' )
r.hset( 'pet:3', 'weapon', 'poison'  )

pipeline = r.pipeline()
pipeline.transaction = True
pipeline.multi()

keys = [ 'pet:1', 'pet:2', 'pet:3' ]

for key in keys: 
    pipeline.hgetall( key )

results = pipeline.execute()

print( '\n\n number of results: {} \n\n'.format( results )  )
for r in results:
    print( r )


print( 'End.' )