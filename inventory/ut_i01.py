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
        inv_Redis  = InvDaoRedis()
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

    def t_04( self ):
        '''Reserve 1 items 

        # before and after running the script see the values in key
        keys inv:dp:1:product:3

        hgetall inv:dp:1:product:3
        
        '''

        cocedis_id = 1
        product_id = 3
        quantity   = 1
        inv_Redis = InvDaoRedis()
        inv_Redis.reserve( cocedis_id, product_id, quantity )


    def t_05( self ):
        '''Take back 1 items '''
        cocedis_id = 1
        product_id = 3
        quantity   = 1
        inv_Redis = InvDaoRedis()
        inv_Redis.take_back( cocedis_id, product_id, quantity )




    def t_06( self ):
        '''Reserve 2 items, it means:
        
        * take 2 items and put them in my cart. 
        * And I continue shopping. I not paying now...

        in redis before test, we must have:
        
        total    : 5 items
        available: 3 items
        reserved : 1 item
        allocated: 1 item

        after test:
        total    : 5 items
        available: 3 - 2 = 1 items
        reserved : 1 + 2 = 3 item
        allocated: 1 item           '''
        pass

    def t_07( self ):
        '''Reserve 3 items, and take back 2. It means:

        * take 3 items and put them in my cart. 
        * take back 2 to the shelf, and my cart must have 1.
        And I continue shopping. I not paying now... '''
        pass

    def t_08( self ):
        '''Reserve 2 items, and pay. It means:

        * take 2 items and put them in my cart. 
        * pay
        * 

        And I continue shopping. I not paying now...'''
        pass


if __name__ == '__main__':
    print( '\n Begin Unit Test.' )
    ut = Ut_i01()
    
    #ut.t_01()
    ut.t_05()

    print( '\n End Unit Test.' )


