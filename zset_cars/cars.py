'''
Here we play with sorted sets and lua scripts.
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
                ,password = REDIS_AUTH
                ,decode_responses= True
                )

# del previous keys
key_cars        = 'cars:speed'
key_tunned_cars = 'tunned:cars:speed'

r.delete( key_cars        )
r.delete( key_tunned_cars )

# create a sorted set called cars:speed
mapping = {
    'ferrari'     : 340,
    'lamborghini' : 350,
    'bugati'      : 360 
}
r.zadd( key_cars, mapping )

# let's use our lua scripts
file_path = '/home/art/git/redis/zset_cars/count_cars.lua'
with open( file_path, 'r' ) as f:
    text = f.read()
count_cars_lua = r.register_script( text )

file_path = '/home/art/git/redis/zset_cars/create_zset.lua'
with open( file_path, 'r' ) as f:
    text = f.read()
create_zset_lua = r.register_script( text )


# get number of cars from our cars sorted set
n = count_cars_lua( keys= [ key_cars ], args = [ REDIS_DB ] )
print( 'number of cars: {}'.format( n ) )


# create a new sorted set called tunned:cars:speed
r = create_zset_lua( keys= [ key_cars, key_tunned_cars ], args = [ REDIS_DB ] ) 
print( r )


# get number of tunned cars cars, our brand new sorted set
n = count_cars_lua( keys= [ key_tunned_cars ], args = [ REDIS_DB ] )
print( 'number of cars: {}'.format( n ) )

print( '\n ... end \n' )
