from CartDaoRedis import CartDaoRedis

class Ut_01:

    def t_01( self ):
        '''get cart items, product_id and quantity in a list'''
        cart = CartDaoRedis()
        a = cart.get_product_qty( client_id = 1 )
        for i in a:
            print( i )

    def t_02( self ):
        '''get products that are in the shopping cart'''
        cart = CartDaoRedis()
        a = cart.get_cart_products( client_id = 1 )
        for i in a:
            print( i )

    def t_03( self ):
        '''get products that are in the shopping cart'''
        cart = CartDaoRedis()
        cart.get_cart_items( client_id = 1 )

    def t_04( self ):
        '''add 1 item to shopping cart'''
        cart = CartDaoRedis()
        client_id           =  1 
        product_id          = 22 
        quantity            =  1 
        override_quantity   = False 
        cart.add( client_id, product_id, quantity, override_quantity )

    def t_05( self ):
        '''update number of items to shopping cart'''
        cart = CartDaoRedis()
        client_id           =  1 
        product_id          = 22 
        quantity            =  9 
        override_quantity   = True
        cart.add( client_id, product_id, quantity, override_quantity )

    def t_06( self ):
        '''remove item from shopping cart'''
        cart = CartDaoRedis()
        client_id           =  1 
        product_id          = 22 
        cart.remove( client_id, product_id )

    def t_07( self ):
        '''remove item from shopping cart'''
        cart = CartDaoRedis()
        client_id           =  1 
        cart.clear( client_id )



if __name__ == '__main__':
    print( '\n Begin Unit Test.' )
    ut = Ut_01()
    ut.t_07()

    print( '\n End Unit Test.' )
