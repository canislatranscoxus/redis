'''
Description: this example connect to a redis database and run a query 
            to search in a redisearch index.

Idea:

    in redis we have mutiple products. Each product stored in a hash with multiple fields.

    product:<product_id>
        name        :
        desciption  :
        uses        :
        benefits    :
        presentation:
        price       :
        .
        .
        .



links:
https://github.com/redis/redis-py/blob/master/tests/test_search.py
'''
from abc import abstractclassmethod, abstractmethod
import os

import redis
import redis.commands.search
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis import Redis
from redis.commands.json.path import Path
from redis.commands.search import Search
from redis.commands.search.field import GeoField, NumericField, TagField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import GeoFilter, NumericFilter, Query
from redis.commands.search.result import Result
from redis.commands.search.suggestion import Suggestion

class Fts():

    @abstractmethod
    def m1( self ):
        pass

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
            print( 'Fts.connect(), error: {}'.format( e ) )
            raise


    def search( self ):
        try:
            self.connect()

            index_name = 'en_product_idx'
            query = 'dog'

            result = self.conn.ft( index_name ).search( query )

            if result != None and result.total > 0:
                for i in result.docs:
                    print( i, '\n' )

            print( 'search done ...' )

        except Exception as e:
            print( 'Fts.search(), error: {}'.format( e ) )
            raise




