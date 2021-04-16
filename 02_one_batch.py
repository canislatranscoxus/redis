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

# make delete these keys before batch.
r.delete( 'animal:eagle' )
r.delete( 'animal:shark' )
r.delete( 'animal:tiger' )

# -----------------------------------------------------------------------------
# Insert key values in redis in a batch
# Begin Batch
pipeline = r.pipeline()
pipeline.transaction = False

pipeline.set( 'animal:eagle', 'fly'  )
pipeline.set( 'animal:shark', 'swim' )
pipeline.set( 'animal:tiger', 'jump' )
pipeline.execute()
# end Batch
# -----------------------------------------------------------------------------

# get data from redis. No batch mode.
print( '\n\n get keys using wildcard animal:*' )
animals = r.scan( cursor = 0, match = 'animal:*'  )[1]
for i in animals:
    print( i )


# ------------------------------------------------------------

# ------------------------------------------------------------


print( '\n\n End \n' )

