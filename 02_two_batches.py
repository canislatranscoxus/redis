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

a = ['animal:eagle'
    ,'animal:shark'
    ,'animal:tiger'
    ,'animal:spider'
    ,'animal:snake'
    ,'animal:cheeta'
    ]
for animal in a:
    r.delete( animal )

# -----------------------------------------------------------------------------
# Insert key values in redis in a batch
# Begin Batch
pipeline = r.pipeline()
pipeline.transaction = False

pipeline.set( 'animal:eagle', 'fly'  )
pipeline.set( 'animal:shark', 'swim' )
pipeline.set( 'animal:tiger', 'jump' )
pipeline.execute()


print( 'starting another batch....' )

pipeline.set( 'animal:spider', 'climb'  )
pipeline.set( 'animal:snake', 'thermal vision' )
pipeline.set( 'animal:cheeta', 'run' )
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

