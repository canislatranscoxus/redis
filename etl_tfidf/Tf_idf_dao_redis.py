import os
import redis

from Key_schema import Key_schema
from Tf_idf_dao_base import Tf_idf_dao_base

class Tf_idf_dao_redis( Tf_idf_dao_base ):

    language        = None
    conn            = None
    pipeline        = None
    key_schema      = None
    del_keys_lua    = None
    count_df_lua    = None
    count_tf_idf_lua= None

    REDIS_HOST      = None 
    REDIS_PORT      = None
    REDIS_DB        = None
    REDIS_AUTH      = None

    def clean_previous_etl( self ):
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

    def ut_insert_token( self ):
        try:
            #
            key1     = self.key_schema.get_tf_key( self.language, 'games' )
            self.conn.set( key1, 'pacman' )

            
            key2     = self.key_schema.get_tf_key( self.language, 'shoes' )
            product_id = 2
            freq    = 22
            mapping = { product_id : freq }
            self.conn.zincrby( key2, freq, product_id )
            

        except Exception as e:
            print( 'Tf_idf_dao_redis.ut_insert_tf(), error: {}'.format( e ) )


    def ut_insert_batch( self, pipeline ):
        try:
            #
            key1     = self.key_schema.get_tf_key( self.language, 'toys' )
            pipeline.set( key1, 'skateboard' )

            
            key2     = self.key_schema.get_tf_key( self.language, 'cars' )
            product_id = 3
            freq    = 33
            mapping = { product_id : freq }
            pipeline.zincrby( key2, freq, product_id )
            

        except Exception as e:
            print( 'Tf_idf_dao_redis.ut_insert_tf(), error: {}'.format( e ) )

    def del_key( self, key ):
        self.conn.delete( key )

    def insert_tf( self, product_id, tfs, pipeline ):
        '''insert the tf of one product in the sorted set key.

        :param string product_id: the id of the product. 
        :param json   tfs       : A dictionary that contains how many times the words occur. 
        :param pipeline pipeline: A redis pipeline. 
        '''
        try:
            for token, freq in tfs.items():
                #print( '{} - {} '.format( token, freq ) )
                key     = self.key_schema.get_tf_key( self.language, token )
                mapping = { product_id : freq }
                pipeline.zincrby( key, freq, product_id )

        except Exception as e:
            print( 'Tf_idf_dao_redis.insert_tf(), error: {}'.format( e ) )
            print( 'product_id: {}'.format( product_id ) )
        

    def count_df( self ):
        try:
            pattern = self.key_schema.get_tf_key( self.language ) + '*'
            
            key     = self.key_schema.get_df_key   ( self.language )
            self.count_df_lua( keys= [ key ], args = [ self.REDIS_DB, pattern ] )

        except Exception as e:
            print( 'Tf_idf_dao_redis.count_df(), error: \n{}\n'.format( e ) )
            raise                    

    def count_tf_idf( self, num_of_products ):
        try:
            df_key        = self.key_schema.get_df_key( self.language )
            pattern       = self.key_schema.get_tf_key( self.language ) + '*'
            tf_idf_prefix = self.key_schema.get_tf_idf_key( self.language )

            #todo fix here. Lua script is not createing tf_idf srted sets

            self.count_tf_idf_lua( keys= [ df_key ], args = [ 
                self.REDIS_DB, pattern, num_of_products, tf_idf_prefix ] )

            print( '\n script executed \n\n' )

        except Exception as e:
            print( 'Tf_idf_dao_redis.count_tf_idf(), error: \n{}\n'.format( e ) )
            raise                    



    def connect( self ):
        try:
            self.REDIS_HOST = os.environ[ 'REDIS_HOST' ]
            self.REDIS_PORT = os.environ[ 'REDIS_PORT' ]
            self.REDIS_DB   = os.environ[ 'REDIS_DB'   ]
            self.REDIS_AUTH = os.environ[ 'REDIS_AUTH' ]

            self.conn = redis.Redis( 
                 host             = self.REDIS_HOST
                ,port             = self.REDIS_PORT
                ,db               = self.REDIS_DB
                ,password         = self.REDIS_AUTH
                ,decode_responses = True
                )

        except Exception as e:
            print( 'Tf_idf_dao_redis.connect(), error: {}'.format( e ) )
            raise


    def create_pipeline( self ):
        pipeline = self.conn.pipeline( transaction = False )
        return pipeline


    def close( self ):
        pass

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


    def __init__( self
                , lua_dir  = '/home/art/git/basmati_gcp/etl_tfidf/lua'
                , language = 'es' ):
        
        self.lua_dir    = lua_dir
        self.language   = language
        self.key_schema = Key_schema()

        self.connect()

        # register lua scripts
        self.del_keys_lua = self.register_lua_script( 'del_keys.lua' )
        self.count_df_lua = self.register_lua_script( 'count_df.lua' )
        self.count_tf_idf_lua = self.register_lua_script( 'count_tf_idf.lua' )




