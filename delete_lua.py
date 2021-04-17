'''
Delete keys that match a pattern using lua scripting.
Strategy: Search and destroy.
'''

import redis
import os
import sys

REDIS_HOST = os.environ[ 'REDIS_HOST' ]
REDIS_PORT = os.environ[ 'REDIS_PORT' ]
#REDIS_DB   = os.environ[ 'REDIS_DB'   ]
REDIS_DB   = 1
REDIS_AUTH = os.environ[ 'REDIS_AUTH' ]


# connect to redis
r = redis.Redis( host     = REDIS_HOST
                ,port     = REDIS_PORT
                ,db       = REDIS_DB
                ,password = REDIS_AUTH
                ,decode_responses= True
                )

print( 'Insert 3 animals, key value pairs in redis ' )
r.set( 'animal:eagle', 'fly'  )
r.set( 'animal:shark', 'swim' )
r.set( 'animal:tiger', 'jump' )

print( '\n\n get keys using wildcard animal:*' )
animals = r.scan( cursor = 0, match = 'animal:*'  )[1]
for i in animals:
    print( i )

# -----------------------------------------------------------------------------
print( 'delete all the animals calling a lua script' )

file_path = '/home/art/git/redis/delete_animals.lua'
with open( file_path, 'r' ) as f:
    text = f.read()

script_delete_animals = r.register_script( text )

# parameters
cursor = 0
pattern = 'animal:*'
db = script_delete_animals ( keys= [ 0 ], args = [ REDIS_DB, cursor, pattern ] )


pattern = 'search*'
db = script_delete_animals ( keys= [ 0 ], args = [ REDIS_DB, cursor, pattern ] )

# -----------------------------------------------------------------------------

print( '\n\n Make sure there are no animals' )
print( 'get keys using wildcard animal:* \n' )
animals = r.scan( cursor = 0, match = 'animal:*'  )[1]
for i in animals:
    print( i )


# ------------------------------------------------------------

# ------------------------------------------------------------


print( '\n\n End \n' )

