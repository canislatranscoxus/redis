from InvDaoRedis import InvDaoRedis

class Ut_i01:

    def t_01( self ):
        '''insert inventory with mocked data.
        See the results in redis insight and see the keys. use the next command:

        keys inv:*
        '''
        inv_Redis = InvDaoRedis()
        #inv_Redis.mock_data()
        inv_Redis.mock_data_8()        

    def t_02( self ):
        ''' delete the inventory of cocedis_id 1
        See the results in redis insight and see the keys. use the next command:

        # before running the script see the keys
        keys inv:dp:1:*

        # after deleting keys, we must wee empty list
        keys inv:dp:1:*        
        '''

        
        inv_Redis  = InvDaoRedis()
        for cocedis_id in range( 8 ):
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
        allocated: 1 item           
        
        #Redis command
        hgetall inv:dp:1:product:3
        '''
        cocedis_id = 1
        product_id = 3
        quantity   = 2
        inv_Redis = InvDaoRedis()
        inv_Redis.reserve( cocedis_id, product_id, quantity )

    def t_07( self ):
        '''Reserve 3 items, and take back 2. It means:

        * take 3 items and put them in my cart. 
        * take back 2 to the shelf, and my cart must have 1.
        And I continue shopping. I not paying now... '''
        cocedis_id = 1
        product_id = 3
        reserve_quantity   = 3
        take_back_quantity = 2
        inv_Redis = InvDaoRedis()
        inv_Redis.reserve  ( cocedis_id, product_id, reserve_quantity )
        inv_Redis.take_back( cocedis_id, product_id, take_back_quantity )

    def t_08( self ):
        '''Reserve 2 items, and pay. It means:

        * take 2 items and put them in my cart. 
        * pay
        * commit sale

        And I continue shopping. I not paying now...'''
        cocedis_id = 1
        product_id = 3
        quantity   = 3
        inv_Redis = InvDaoRedis()
        inv_Redis.reserve    ( cocedis_id, product_id, quantity )
        inv_Redis.commit_sale( cocedis_id, product_id, quantity )

    def t_09( self ):
        '''Commit sale of all the items in the shopping cart. It means:

        * take 2 items of the same product_id and put them in my cart. 
        * take 1 items with different product_id and put them in my cart. 
        * pay
        * commit sale

        # redis commands
        hgetall inv:dp:1:product:3
        hgetall inv:dp:1:product:5
        '''

        cocedis_id=1
        inv_Redis = InvDaoRedis()
        inv_Redis.reserve    ( cocedis_id, product_id=3, quantity=3 )
        inv_Redis.reserve    ( cocedis_id, product_id=5, quantity=1 )
        cart_items= [
            { 'cocedis_id': cocedis_id, 'product_id': 3, 'quantity': 3 },
            { 'cocedis_id': cocedis_id, 'product_id': 5, 'quantity': 1 },
        ]
        inv_Redis.commit_cart_sale( cart_items )

    def t_10( self ):
        inv_Redis = InvDaoRedis()
        inv_Redis.pass_dic()

    def t_11( self ):
        inv_Redis = InvDaoRedis()

        cocedis_id = 8
        id_qty      = {
            '1'  : 2,
            '2'  : 3,
        }
        inv_Redis.mock_data_x( cocedis_id, 1 )
        inv_Redis.mock_data_x( cocedis_id, 2 )

        inv_Redis.update_inv_out( cocedis_id, id_qty )
        print( 'ut 11 ok' )

    def t_12( self ):
        # set initial inventory.

        inv_Redis = InvDaoRedis()

        cocedis_id = 8
        inv_Redis.mock_data_x( cocedis_id, 1 )
        inv_Redis.mock_data_x( cocedis_id, 2 )
        inv_Redis.mock_data_x( cocedis_id, 3 )

        print( 'ut 12 ok' )



if __name__ == '__main__':
    print( '\n Begin Unit Test.' )
    ut = Ut_i01()
    
    #ut.t_03()
    #ut.t_01()
    #ut.t_02()

    ut.t_12()

    print( '\n End Unit Test.' )


