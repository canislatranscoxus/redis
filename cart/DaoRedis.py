'''
description: Inventory Strategy 3. One hash per Cocedis and product.
             This is simplest and fastest.
             And other user will not be waiting while they buy other products.


            This script connect to  Redis and set the inventaory of All cocedis.
             We specify the amount of total, available, reserved, allocated values per each product.


To delete this keys in redis use the command below 

del inv_cocedis:1 inv_cocedis:2 inv_cocedis:3 inv_cocedis:4 inv_cocedis:5 inv_cocedis:6

'''


import os
from typing import Mapping
import redis



num_of_cocedis  = 6
num_of_products = 31

class DaoRedis:

    keySchemaInv         = None
    del_keys_lua         = None
    reserve_lua          = None
    take_back_lua        = None
    commit_sale_lua      = None
    commit_cart_sale_lua = None
    add_available_lua    = None
    update_available_lua = None

    REDIS_HOST      = None 
    REDIS_PORT      = None
    REDIS_DB        = None
    REDIS_AUTH      = None


    def connect( self ):
        try:
            self.REDIS_HOST = os.environ[ 'REDIS_HOST' ]
            self.REDIS_PORT = os.environ[ 'REDIS_PORT' ]
            self.REDIS_DB   = os.environ[ 'REDIS_DB'   ]
            self.REDIS_AUTH = os.environ[ 'REDIS_AUTH' ]

            self.conn = redis.StrictRedis( 
                 host             = self.REDIS_HOST
                ,port             = self.REDIS_PORT
                ,db               = self.REDIS_DB
                ,password         = self.REDIS_AUTH
                ,decode_responses = True
                )


        except Exception as e:
            print( 'Cart.connect(), error: Redis connection is None' )
            raise

    def create_pipeline( self, transaction = False ):
        pipeline = self.conn.pipeline( transaction )
        return pipeline

    def register_lua_script( self, file_name ):
        try:
            file_path = os.path.join( self.lua_dir, file_name )
            with open( file_path, 'r' ) as f:
                text = f.read()
            
            script = self.conn.register_script( text )
            return script
        except Exception as e:
            print( 'Tf_idf_dao_redis.register_lua_script(), error: {}'.format( e ) )
            raise

    def delete_keys( self, prefix ):
        '''In redis, delete all the keys related to the previous etl proces of an specific language.

        we use the attribute language: A string of 2 characters specifieng the human language used.
            For example: 
                en English, 
                sp Spanish, 
                ko Korean, 
                hi Hindi.
        '''
        try:
            prefix  = self.keySchemaInv.get_prefix( )
            # For all the etls, for all the languages use the line below
            #prefix = Key_schema.prefix

            pattern = '{}*'.format( prefix )
            result  = self.del_keys_lua( keys= [ 0 ], args = [ self.REDIS_DB, pattern ] )

        except Exception as e:
            print( 'InvDaoRedis().delete_keys, error: {}'.format( e ) )
            raise


    def run_lua_script( self, cocedis_id, product_id, quantity ):
        try:
            '''key    = self.keySchemaInv.get_inventory_key( cocedis_id, product_id )
            result = self.script_lua( keys = [key], args = [ self.REDIS_DB, p2, p3 ] )'''
            print( ' run your script ' )

        except Exception as e:
            print( 'InvDaoBase.run_lua_script(), error: {}'.format( e ) )
            raise






    def __init__(self, params=None ) -> None:
        self.lua_dir      = '/home/art/git/redis/cart/lua'
        #self.keySchemaInv = KeySchemaInv()

        self.connect( )

        # register lua scripts
        self.del_keys_lua = self.register_lua_script( 'del_keys.lua' )
        #self.script_lua   = self.register_lua_script( 'my_script.lua' )







