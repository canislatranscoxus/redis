from Cart import Cart

class Ut_01:

    def t_01( self ):
        '''get cart items, product id and quantity in a list'''
        cart = Cart()
        cart.get_cart_items_qty( client_id = 1 )

    def t_02( self ):
        '''get products that are in the shopping cart'''
        cart = Cart()
        cart.get_cart_products( client_id = 1 )

    def t_03( self ):
        '''get products that are in the shopping cart'''
        cart = Cart()
        cart.get_cart_items( client_id = 1 )


if __name__ == '__main__':
    print( '\n Begin Unit Test.' )
    ut = Ut_01()
    ut.t_03()

    print( '\n End Unit Test.' )
