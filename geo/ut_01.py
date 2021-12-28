import os
from Gps_ov import Gps_ov



class Ut_cocedis:
    def t_01( self ):

        params = {
            'REDIS_HOST' : os.environ[ 'REDIS_HOST' ],
            'REDIS_PORT' : os.environ[ 'REDIS_PORT' ],
            'REDIS_DB'   : os.environ[ 'REDIS_DB'   ],
            'REDIS_AUTH' : os.environ[ 'REDIS_AUTH' ],
        }


        gps = Gps_ov( params )

        print( type( gps ) )

        result = gps.find_stores( 
          longitude   = '-100.38365162311239'
        , latitude    = '25.661906044204862'
        , top_n       =  10
        , radius      = 200
        , radius_unit = 'km' )

        
        print( type( result ) )
        print( result )

        for i in result:
            print( 'store: {}, {} km, lon: {}, lat: {}'.format( i[0], i[1], i[2][0], i[2][1] ) )



if __name__ == '__main__':
    print( '\n Begin Unit Test.' )
    ut = Ut_cocedis()
    ut.t_01()
    print( '\n End Unit Test.' )


