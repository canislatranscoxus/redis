'''
Here we delete all the keys that match the pattern 'animal*'
Using the python library. No pipeline. No optimization.

The strategy is scan all the keys that match the pattern,
then delete one by one.

A better approach is use a pipeline.
But the most efficient is using Lua scripts.

'''

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

# Insert key values in redis
r.set( 'animal:eagle', 'fly'  )
r.set( 'animal:shark', 'swim' )
r.set( 'animal:tiger', 'jump' )

value = r.get( 'animal:eagle' )
print( '\n\n animal:eagle is {}'.format( value ) )

print( '\n\n get keys using wildcard animal:*' )
animals = r.scan( cursor = 0, match = 'animal:*'  )[1]
for i in animals:
    print( i )

print( '\n\n get values passing keys' )
values = r.mget( animals )
for i in values:
    print( i )

# delete all the animals

keys = r.scan_iter( match = 'animal*' )
for key in keys:
    r.delete( key )

print( '\n\n get keys using wildcard animal:*' )
animals = r.scan( cursor = 0, match = 'animal:*'  )[1]
for i in animals:
    print( i )


# ------------------------------------------------------------

# ------------------------------------------------------------


print( '\n\n End \n' )

