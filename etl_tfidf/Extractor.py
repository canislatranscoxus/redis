import pymysql.cursors

import os

MYSQL_NAME     = os.environ[ 'MYSQL_NAME'     ]
MYSQL_USER     = os.environ[ 'MYSQL_USER'     ]
MYSQL_PASSWORD = os.environ[ 'MYSQL_PASSWORD' ]
MYSQL_HOST     = os.environ[ 'MYSQL_HOST'     ]


class Extractor:

    conn = None
    
    # en, es
    language_code = None

    # product id range. None range means, bring all the products.
    start_id = None
    end_id   = None 

    sql_base = """  SELECT {fields}
                    FROM  shop_product p 
                    JOIN  shop_product_translation t
                    ON 	  p.id = t.master_id
                    WHERE t.language_code = '{language}'
               """

    cursor = None

    def connect( self ):
        # Connect to the database
        self.conn = pymysql.connect(host        = MYSQL_HOST,
                                    user        = MYSQL_USER,
                                    password    = MYSQL_PASSWORD,
                                    database    = MYSQL_NAME,
                                    charset     = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor )

    def get_num_of_products( self ):
        try:
            d = {
                    'fields'   : 'count(*) ',
                    'language' :  self.language_code
            }   
            sql              = self.sql_base.format( **d )
            cursor           = self.conn.cursor()
            number_of_rows   = cursor.execute(sql)
            row              = cursor.fetchone(  )
            num_of_products  = int( row[ 'count(*)' ] )
            return num_of_products

        except Exception as e:
            print( 'Extractor.get_num_products(), error: {}'.format( e ) )
        

    def execute( self ):
        try:

            '''where_clause = ''
            if self.language_code != None:
                where_clause = " WHERE t.language_code = '{}' ".format( self.language_code )

            if self.start_id != None and self.end_id != None :
                if where_clause == '':
                    where_clause = ' WHERE '
                else: 
                    where_clause = where_clause + ' AND '

                where_clause = "{} p.id >= {} and p.id <= {}".format( 
                    where_clause, self.start_id, self.end_id )'''

            d = {
                'fields'   : 'p.id, p.by, t.language_code, t.name, t.description ',
                'language' :  self.language_code
            }   

            sql             = self.sql_base.format( **d )
            self.cursor     = self.conn.cursor()
            number_of_rows  = self.cursor.execute(sql)

            print( 'query: \n\n {} \n\n'.format( sql ) )
            print( 'sql execute, number of rows: {}'.format( number_of_rows ) )

        except Exception as e:
            print( 'Extractor.execute(), error: {}'.format( e ) )


    def get_next_row( self ):
        pass

    def get_next_batch( self, num_of_rows = 20 ):
        '''
        get the next batch of rows using the

        :param int num_of_rows: The number of rows per batch
        '''
        try:
            rows = self.cursor.fetchmany( num_of_rows )
            return rows
            
        except Exception as e:
            print( 'Extractor.get_many(), error: {}'.format( e ) )
            self.conn.close()

    def close( self ):
        try:
            self.conn.close()
        except Exception as e:
            print( 'Extractor.close(), error: {}'.format( e ) )

    def __init__( self, language ):
        self.language_code = language