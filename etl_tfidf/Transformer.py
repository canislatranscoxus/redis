import json
import os
import unidecode


class Transformer:

    language    = None
    stop_words  = None

    def get_tf( self, product ):
        '''
        Count words. Get the Token Frequency. Take as input json representing product,
        and return a dictionary that contains the frequency of each token in a product (document).

        :param json product: A json that represent a product
        '''
        d = {}
        
        try:
            tokens = self.get_tokens( product )
            for word in tokens:
                if word in d:
                    d[ word ] = d[ word ] + 1
                else:
                    d[ word ] = 1

            return d

        except Exception as e:
            print( 'Transformer.get_tf(), error: {}'.format( e ) )


    def clean_text( self, row_string ):
        try:
            #
            s = unidecode.unidecode( row_string.lower() ) 
            a = s.split()
            return a
        except Exception as e:
            print( 'Transformer.clean_text(), error: {}'.format( e ) )


    def get_tokens( self, product ):
        ''' 
        get the tokens of a product using the next attributes: by, name and description.

        :param json product: A json that represent a product
        '''

        try:
            
            row_data = self.clean_text( product[ 'by'          ] ) \
                     + self.clean_text( product[ 'name'        ] ) \
                     + self.clean_text( product[ 'description' ] ) 

            # remove commas, periods, etc
            separators = [ '.', ',', ':', ';' ]
            a = []
            for word in row_data:
                if word[ -1 ] in separators:
                    a.append( word[ : -1 ] )
                else:
                    a.append( word )  

            tokens = [word for word in a if word not in self.stop_words ]

            return tokens
        except Exception as e:
            print( 'Transformer.get_tokens(), error: {}'.format( e ) )
        

    '''def create_stop_words( self ):

        input_file = '/home/art/git/basmati_gcp/etl_tfidf/temp.txt'
        output_file = '/home/art/git/basmati_gcp/etl_tfidf/stop_words.txt'

        a = None
        with open( input_file, 'r') as f:
            lines = [ line.rstrip() for line in f ]
            lines.sort()

        with open( output_file, 'w' ) as f:
            for word in lines:
                f.write( word + '\n' )
    '''

    def __init__( self
        , stop_words_dir = '/home/art/git/basmati_gcp/etl_tfidf/stop_words'
        , language       = 'es' ):

        try:
            file_name = f'{language}.txt'
            file_path = os.path.join( stop_words_dir, file_name )

            with open( file_path, 'r') as f:
                self.stop_words  = [ i.strip() for i in f.readlines(  ) ]

        except Exception as e:
            print( 'Transformer.__init__(), error: {}'.format( e ) )
            raise

if __name__ == '__main__':
    t = Transformer()
    
    print( '\n\n transformer... end. \n' )