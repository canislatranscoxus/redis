import json
import os
import sys

import redis
import redis.commands.search
import redis.commands.search
import redis.commands.search.aggregation as aggs
import redis.commands.search.reducers    as reducers
from   redis.commands.search.query       import NumericFilter, Query
from   redis.commands.search.querystring import querystring


# Connect to Redis Database
REDIS_HOST = os.environ[ 'REDIS_HOST' ]
REDIS_PORT = os.environ[ 'REDIS_PORT' ]
REDIS_DB   = os.environ[ 'REDIS_DB'   ]
REDIS_AUTH = os.environ[ 'REDIS_AUTH' ]

print( 'basmati.settings.py redis' )
print( 'REDIS_HOST: {}'.format( REDIS_HOST ) )
print( 'REDIS_PORT: {}'.format( REDIS_PORT ) )
print( 'REDIS_DB  : {}'.format( REDIS_DB   ) )
print( 'REDIS_AUTH: {}'.format( REDIS_AUTH ) )


conn = redis.Redis(
     host             = REDIS_HOST
    ,port             = REDIS_PORT
    ,db               = REDIS_DB
    ,password         = REDIS_AUTH
    ,decode_responses = True
    )



db_index = 'product_idx'
# query = '@password:(123)'
# results = conn.ft( db_index ).search( query )
# print( results )



def select_products( ):
    # Get the last 10 orders of the client. Only order, no items. See sql
    #
    # SELECT *
    # FROM my_order_index
    # WHERE client_id =   <client_id>
    # and row_num between offset and (offset + num)
    # SORT BY order_id DESC
    # LIMIT 10
    try:
        offset = 0
        num    = 10
        where  = '@product_id:[ 1 100 ]'
        query  = (  Query( where )
                    .return_fields( 'product_id', 'name', 'pic' )
                    .paging(offset, num)
                    .sort_by( 'product_id' , asc=False)
                  )

        # query = (Query(q).return_fields(  )
        #          .paging(offset, num).sort_by('order_id', asc=False))

        result = conn.ft( db_index ).search( query )

        print( result )

        return result
    except Exception as e:
        print( 'select_products(), error: {}'.format(e) )

# Unit Testing

p = select_products()

print( 'End' )