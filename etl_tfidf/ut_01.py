import json
from Extractor          import Extractor
from Transformer        import Transformer
from Key_schema         import Key_schema
from Tf_idf_dao_redis   import Tf_idf_dao_redis


def c_01():
    '''get batches of rows from mySQL database. '''
    try:

        e = Extractor()
        e.connect()
        e.execute()
        rows = e.get_next_batch( num_of_rows= 2 )

        while len( rows ) > 0:

            print( '\n ut_01.c_01(), looping BATCH of rows' )

            for r in rows:
                print( '\n {}'.format( r ) )

            rows = e.get_next_batch( num_of_rows= 2 )

        e.close()

    except Exception as e:
        print( 'ut_01.c_01(), error: {}'.format( e ) )

    print( '\n end of case 1.' )

def c_02():
    ''' transform from json to string list. Take as input a product in a json, 
    and return as output a list of strings, each string is a token. We use 
    the attributes: by, name, description.'''

    try:
        j_es = { 
                'id'            : 2, 
                'by'            : 'khazana', 
                'language_code' : 'es', 
                'master_id'     : 2, 
                'name'          : 'Khazana arroz Basmati', 
                'description'   : '10 libras 4,53 kg. Arroz Basmati premium extra largo. El tesoro.'
            }

        j = { 
                'id'            : 2, 
                'by'            : 'khazana', 
                'language_code' : 'en', 
                'name'          : 'Khazana Basmati rice', 
                'description'   : '10 lb 4.53 kg. Extra long premium Basmati Rice. The Treasure.'
            }

        t = Transformer()
        tokens = t.get_tokens( j )

        print( '\n case 02. Tokens: {} \n'.format( tokens ) )


    except Exception as e:
        print( 'c_02(), error: {}'.format( e ) )

def c_03():
    ''' Transformer.get_tf()
    '''

    try:
        j = { 
                'id'            : 2, 
                'by'            : 'khazana', 
                'language_code' : 'en', 
                'name'          : 'Khazana Basmati rice', 
                'description'   : '10 lb 4.53 kg. Extra long premium Basmati Rice. The Treasure.'
            }

        t = Transformer()
        d = t.get_tf ( j )

        print( '\n case 03. tf: \n {} \n'.format( json.dumps( d, indent = 3) ) )
    except Exception as e:
        print( 'c_03(), error: {}'.format( e ) )

def c_04():
    ''' key schemas
    '''
    try:
        key_schema = Key_schema()
        
        language = 'es'

        keys = []
        keys.append( key_schema.get_tf_key    ( language , token = 'basmati'))
        keys.append( key_schema.get_df_key    ( language                    ))
        keys.append( key_schema.get_tf_idf_key( language , token = 'sushi'  ))

        keys.append( key_schema.get_tf_key    ( language  ))
        keys.append( key_schema.get_tf_idf_key( language  ))


        for i in keys:
            print( i + '***' )

    except Exception as e:
        print( 'c_04(), error: {}'.format( e ) )

def c_05():
    ''' delete previous etl
    '''
    try:
        t = Tf_idf_dao_redis()
        t.connect()

        #t.ut_insert_token()   

        pipeline = t.create_pipeline()
        
        t.ut_insert_batch( pipeline )
        pipeline.execute()

        t.clean_previous_etl()

    except Exception as e:
        print( 'c_05(), error: {}'.format( e ) )

def c_06():
    ''' Count Document Frequencies per Term
    '''
    try:
        t = Tf_idf_dao_redis()
        t.connect()
        t.count_df()

    except Exception as e:
        print( 'c_06(), error: {}'.format( e ) )

def c_07():
    ''' get number of products
    '''
    try:
        extractor = Extractor( language = 'es' )
        extractor.connect()
        n = extractor.get_num_of_products()
        print( n )
    except Exception as e:
        print( 'c_06(), error: {}'.format( e ) )



if __name__ == '__main__':

    #c_02()
    #c_03()
    c_04()
    #c_05()
    #c_06()
    #c_07()


    print( '\n end of Unit Test.' )
