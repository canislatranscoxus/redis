'''
Description: This class is used to located the closest stores or warehouses.
             Behind the scenes this component makes a connection to redis,
             and call GEOSEARCH to get the top N places we want.

links:
    https://code.tutsplus.com/tutorials/building-a-store-finder-with-nodejs-and-redis--cms-26283
    https://sw-ke.facebook.com/groups/1503702279845839/
    https://redis-py.readthedocs.io/en/stable/redis_commands.html?highlight=geosearch#redis.commands.core.CoreCommands.geosearch
'''
import os
import redis
from   redisearch import Client, TextField, IndexDefinition, Query



#import sys
#from django.conf import settings


#from .Key_schema import Key_schema 


#todo: code this class 

class Gps_ov:
    conn            = None
    STORES_KEY      = 'geo_shop'      # a set with shops geo coordinates
    WAREHOUSES_KEY  = 'geo_warehouse' # a set with black warehouses geo coordinates

    def find_warehouse( self, lon_user, lat_user, top_n=10 ):
        pass

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
            print( 'Redis connection is None' )
            raise

    
    def transform_geosearch_response( self, response):
        a = [{"store": item[0], "distance": item[1], "location": {"latitude": item[1][1], "longitude": item[1][0]}} for item in response]
        return a
    


    def geosearch( self, key, longitude, latitude, top_n=10, radius = 200, radius_unit='km' ):
        '''Execute the geosearch redis command.        '''
        try:
            cmd = f'''
                geosearch   {key} 
                fromlonlat  {longitude} {latitude} 
                byradius    {radius} {radius_unit} 
                ASC 
                COUNT       {top_n}
                WITHCOORD WITHDIST'''

            results = self.conn.execute_command( cmd )
            return results

        except Exception as e:
            print( 'Gps_ov.geosearch(), error: {}'.format( e ) )
            raise


    def find_stores( self, longitude, latitude, top_n=10, radius = 2000, radius_unit='km' ):
        '''Get the top N stores closest to client. 
        The client coordinates are  lon_user, lat_user'''
        try:
            results = self.geosearch( self.STORES_KEY, longitude, latitude, top_n=10, radius = 200, radius_unit='km' )
            a = self.transform_geosearch_response( results )
            return a

        except Exception as e:
            print( 'Gps_ov.find_stores(), error: {}'.format( e ) )
            raise

    def __init__(self, params = None ) -> None:
        try:
            self.connect( params )
            print( 'Gps_ov.__init__() ... ok' )

        except Exception as e:
            print( 'Gps_ov.__init__(), error: {}'.format( e ) )
            raise



