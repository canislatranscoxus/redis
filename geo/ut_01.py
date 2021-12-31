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

        stores = gps.find_stores( 
          longitude   = '-100.38365162311239'
        , latitude    = '25.661906044204862'
        , top_n       =  10
        , radius      = 200
        , radius_unit = 'km' )

        
        print( type( stores ) )
        print( stores, '\n' )
        

        for i in stores:
            print( i )



if __name__ == '__main__':
    print( '\n Begin Unit Test.' )
    ut = Ut_cocedis()
    ut.t_01()
    print( '\n End Unit Test.' )


