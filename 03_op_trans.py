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

''' 
There are 2 styles to write the code for Optimistic Transactions:

1) using pipelines, watch, multi, exec

2) using the Transaction method 
'''

def ut_transaction_1(  ):
    # make delete these keys 
    r.delete( 'my_pet' )
    r.set( 'my_pet', 'dog' )

    # redis Optimistic Transaction
    pipeline = r.pipeline()
    pipeline.transaction = True

    # watch that this key does not change
    pipeline.watch( 'my_pet' )

    # begin of transaction
    pipeline.multi()

    pipeline.set( 'my_pet', 'cat'  )
    pipeline.set( 'my_pet', 'tiger'  )

    # if my_pet was not changes before begin of transaction, execute the commands 
    pipeline.execute()
    # end of transaction
    # -----------------------------------------------------------------------------

    # get data from redis. No batch mode.
    val = r.get( 'my_pet' )
    print( 'ut_1) my_pet is: {}'.format( val ) )


# ------------------------------------------------------------
# style 2.


def transaction_func( pipeline: redis.client.Pipeline) -> None:
    pipeline.multi()
    pipeline.set( 'my_pet', 'cat'  )
    pipeline.set( 'my_pet', 'tiger'  )
    pipeline.execute()




def ut_transaction_2(  ):
    # make delete these keys 
    r.delete( 'my_pet' )
    r.set( 'my_pet', 'dog' )

    # redis Optimistic Transaction
    r.transaction(transaction_func, *[ 'my_pet'  ])
    # -----------------------------------------------------------------------------

    # get data from redis. No batch mode.
    val = r.get( 'my_pet' )
    print( 'ut_2) my_pet is: {}'.format( val ) )


# ------------------------------------------------------------

ut_transaction_1()
ut_transaction_2()

print( '\n\n End \n' )

