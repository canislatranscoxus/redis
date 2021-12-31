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
import redis


num_of_cocedis  = 6
num_of_products = 31

class InvDaoRedis:

    def connect( self, params ):
        try:
            if params == None:
                params = {
                    'REDIS_HOST'  : os[ 'REDIS_HOST' ],
                    'REDIS_PORT'  : os[ 'REDIS_PORT' ],
                    'REDIS_DB'    : os[ 'REDIS_DB'   ],
                    'REDIS_AUTH'  : os[ 'REDIS_AUTH' ],
                }

            self.conn = redis.StrictRedis(
                  host              = params[ 'REDIS_HOST' ]
                , port              = params[ 'REDIS_PORT' ]
                , db                = params[ 'REDIS_DB'   ]
                , password          = params[ 'REDIS_AUTH' ]
                , charset           = "utf-8"
                , decode_responses  = True
                )

        except Exception as e:
            print( 'InvDaoBase.connect(), error: Redis connection is None' )
            raise


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
            prefix = self.key_schema.get_prefix( self.language  )
            # For all the etls, for all the languages use the line below
            #prefix = Key_schema.prefix

            pattern = '{}*'.format( prefix )
            result  = self.del_keys_lua( keys= [ 0 ], args = [ self.REDIS_DB, pattern ] )

        except Exception as e:
            print( 'Tf_idf_redis().clean_previous_etl, error: {}'.format( e ) )
            raise


    def del_inventory( self, cocedis_id = None ):
        pass



    def reserve_item( self, cocedis, product_id, quantity ):
        pass

    def take_back_item( self, cocedis, product_id, quantity ):
        pass

    def add_update_cocedis( self, cocedis_id, product_inv_list ):
        '''Add or update the inventory of One cocedis. This method must be called when a
        Distribution Point is starting, or need to update their real inventory.

        cocedis_id : int. 
         '''
        pass

    def mock_data_cocedis( self, pipe, cocedis_id = 1 ):
        '''Initialize the inventory with mocked data, dummy data.'''

        try:
            d = {
                'cocedis_id' : 0,
                'product_id' : 0,
                'total'      : 5,
                'available'  : 3,
                'reserved'   : 1,
                'allocated'  : 1,
                }

            s = '''HSET inv:dp:{cocedis_id}:product:{product_id} total {total} available {available} reserved {reserved} allocated {allocated}'''

            for product_id in range( 1, num_of_products + 1 ):

                d[ 'cocedis_id' ] = cocedis_id
                d[ 'product_id' ] = product_id
                cmd               = s.format( **d )
                print( cmd )

                # add command to pipe


        except Exception as e:
            print( 'InvDaoBase.mock_data_cocedis(), error: {}'.format( e ) )
            raise



    def mock_data( self ):
        '''Insert mocked data, dummy data for 6 cocedis'''
        cocedis_id = 1

        try:

            for cocedis_id in range( 0, 7 ):
                # create pipe
                pipe = None

                self.mock_data_cocedis( pipe, cocedis_id )

                #execute batch
                pipe.execute_batch()

        except Exception as e:
            print( 'InvDaoBase.mock_data(), error: {}'.format( e ) )
            raise

    def __init__(self, params ) -> None:
        self.lua_dir    = params[ 'lua_dir' ]
        self.key_schema = Key_schema()

        self.connect( params )

        # register lua scripts
        self.del_keys_lua = self.register_lua_script( 'del_keys.lua' )
        self.count_df_lua = self.register_lua_script( 'count_df.lua' )





