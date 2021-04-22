'''
This auxiliar file contains some functions and helpful tools to create files or test something

pip install 

stopwordsiso
Unidecode

'''

# create stop words file for  other languages

import os
import stopwordsiso as stopwords
import unidecode

stopwords.has_lang("th")  # check if there is a stopwords for the language
stopwords.langs()  # return a set of all the supported languages
stopwords.stopwords("en")  # English stopwords

class Stop_words:

    language = None

    def get_words( self ):
        result = stopwords.stopwords( self.language )  
        return result

    def remove_accents( self, row_data ):

        s = set()
        for i in row_data:
            word = unidecode.unidecode( i.lower() )
            s.add( word )

        return s

    def save( self, words ):
        sw_dir = '/home/art/git/basmati_gcp/etl_tfidf/stop_words'
        file_name = f'{self.language}.txt'
        file_path = os.path.join( sw_dir, file_name )

        with open( file_path, 'w') as f:
            for word in words:
                f.write( word + '\n' )
        
        print( 'file created: {}'.format( file_path ) )

    def run( self ):
        try:
            row_data = self.get_words()
            s = self.remove_accents( row_data )

            words = list( s )
            words.sort()

            #self.save( words )
        except Exception as e:
            print( 'Stop_words.run(), error: {}'.format( e ) )
            raise
         

    def __init__( self, language ):
        self.language = language


if __name__ == '__main__':
    stop_words = Stop_words( language= 'es' )
    stop_words.run()
    print( 'tool_01, ... end \n' )