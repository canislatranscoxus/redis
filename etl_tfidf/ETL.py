from Extractor        import Extractor
from Transformer      import Transformer
from Tf_idf_dao_redis import Tf_idf_dao_redis


class ETL:

    # attributes

    # etl
    persist_2_redis = True
    persist_2_csv   = True
    output_folder   = ''
    is_cloud        = False

    # loader
    loader          = None
    is_kill_n_fill  = True
    language        = 'es'
    lua_dir         = '/home/art/git/basmati_gcp/etl_tfidf/lua'


    # ------------------------------------------------------------------------------
    # methods 
    # ------------------------------------------------------------------------------

    def clean_previous_etl( self, ):
        if self.is_kill_n_fill == True:
            self.loader.clean_previous_etl( )

    def persist( self, ):
        pass

    '''def extract( self, ):
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
    '''
    



    def process_all( self ):
        try:
            print( 'process_all ... begin' )

            extractor       = Extractor( self.language  )
            transformer     = Transformer()
            extractor.connect()
            num_of_products = extractor.get_num_of_products()

            extractor.execute()
            num_of_rows     = 10
            rows            = extractor.get_next_batch( num_of_rows )
            pipeline        = self.loader.create_pipeline()

            while len( rows ) > 0:

                for product in rows:
                    print( '\n {}'.format( product ) )

                    tf  = transformer.get_tf( product )
                    print( 'len tf: {}'.format( len( tf ) ) )
                    self.loader.insert_tf( product[ 'id' ], tf, pipeline )

                pipeline.execute()
                rows = extractor.get_next_batch( num_of_rows )

            extractor.close()
            self.loader.count_df( )
            self.loader.count_tf_idf( num_of_products )

        except Exception as e:
            print( 'ETL.process_all(), error: {}'.format( e ) )


    def process_new( self, product_range  ):
        pass

    def run( self ):
        #self.loader.connect()

        if self.is_kill_n_fill:

            self.clean_previous_etl()
            self.process_all()
        else:
            self.process_new()
        

    def __init__( self ):
        # set attributes
        print( 'ETL.__init__()' )
        self.loader      = Tf_idf_dao_redis()





