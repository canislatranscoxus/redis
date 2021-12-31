from InvDaoRedis import InvDaoRedis

class Ut_i01:

    def t_01( self ):
        '''insert inventory with mocked data.
        See the results in redis insight and see the keys. use the next command:

        keys inv:*
        '''

        inv_Redis = InvDaoRedis()
        inv_Redis.mock_data()


    def t_02( self ):
        ''' delete the inventory of cocedis_id 1
        See the results in redis insight and see the keys. use the next command:

        # before running the script see the keys
        keys inv:dp:1:*

        # after deleting keys, we must wee empty list
        keys inv:dp:1:*        
        '''

        cocedis_id = 1
        inv_Redis = InvDaoRedis()
        inv_Redis.del_inventory( cocedis_id )

    def t_03( self ):
        ''' delete the inventory of all the cocedis
        See the results in redis insight and see the keys. use the next command:

        # before running the script see the keys
        keys inv:*

        # after deleting keys, we must wee empty list
        keys inv:*
        '''

        inv_Redis = InvDaoRedis()
        inv_Redis.del_inventory(  )



if __name__ == '__main__':
    print( '\n Begin Unit Test.' )
    ut = Ut_i01()
    ut.t_03()
    print( '\n End Unit Test.' )


