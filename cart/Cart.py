'''
description: Inventory Strategy 3. One hash per Cocedis and product.
             This is simplest and fastest.
             And other user will not be waiting while they buy other products.


            This script connect to  Redis and set the inventaory of All cocedis.
             We specify the amount of total, available, reserved, allocated values per each product.


To delete this keys in redis use the command below 

del inv_cocedis:1 inv_cocedis:2 inv_cocedis:3 inv_cocedis:4 inv_cocedis:5 inv_cocedis:6

'''


import os
from typing import Mapping
import redis

from DaoRedis       import DaoRedis
from KeySchemaCart  import KeySchemaCart


num_of_cocedis  = 6
num_of_products = 31

class Cart( DaoRedis ):

    keySchemaCart          = None
    del_keys_lua           = None
    get_cart_items_lua     = None    
    get_cart_items_qty_lua = None
    get_cart_products_lua  = None

    REDIS_HOST      = None 
    REDIS_PORT      = None
    REDIS_DB        = None
    REDIS_AUTH      = None



    def format_redis_items( self, row_list ):
        '''Format the cart items,
        input : result from redis. Row list.
        output: dictionary of dictionary'''
        try:
            #
            d = {}
            for i in range( 0, len(row_list), 2  ):
                item = { 
                    'quantity' : row_list[ i + 1 ]
                 }
                d[ row_list[ i ] ] = item
            
            return d

        except Exception as e:
            print( 'Cart.product_qty_2_dic(), error: {}'.format( e ) )
            raise


    def list_2_dic( self, row_list ):
        '''Convert list to dictionary'''
        try:
            #
            d = {}
            for i in range( 0, len(row_list), 2  ):
                d[ row_list[ i ] ] = row_list[ i + 1 ]
            return d

        except Exception as e:
            print( 'Cart.product_qty_2_dic(), error: {}'.format( e ) )
            raise

    def found_products_2_list( self, row_list ):
        '''Take as input the found products from redis and 
        return as output the products data as a list of dictionaries'''

        try:
            d = {}
            if row_list == None or len( row_list ) < 3:
                return d
            
            for i in range( 1, len( row_list )-1, 2 ):
                id      = self.keySchemaCart.get_product_id_from_search_box_key( row_list[ i ] )
                product = self.list_2_dic( row_list[ i + 1 ] )
                d[ id ] = product

            return d

        except Exception as e:
            print( 'Cart.product_qty_2_dic(), error: {}'.format( e ) )
            raise

    def get_cart_items( self, client_id  ):
        try:
            '''key    = self.keySchemaInv.get_inventory_key( cocedis_id, product_id )'''
            key = 'cart:client:{}' .format( client_id )
            result = self.get_cart_items_lua( keys = [key], args = [ self.REDIS_DB ] )
            #print( result )

            items        = self.list_2_dic( result[ 0 ] )
            dod_products = self.found_products_2_dics( result[ 1 ] )

            # todo: Add product to items
            '''
            products = self.dod_products_2_objs( dod_products )
            for k, v in items.items():
                v[ 'product' ] = products[ k ]
            '''

            print( '..\n' )
            
        except Exception as e:
            print( 'Cart.get_items_qty(), error: {}'.format( e ) )
            raise

    def get_cart_items_qty( self, client_id  ):
        ''' Used for Unit Testing.
            Get product_id and qty, for all the cart items.
        '''
        try:
            '''key    = self.keySchemaInv.get_inventory_key( cocedis_id, product_id )'''
            key = 'cart:client:{}' .format( client_id )
            result = self.get_cart_items_qty_lua( keys = [key], args = [ self.REDIS_DB ] )
            print( result )
            
        except Exception as e:
            print( 'Cart.get_items_qty(), error: {}'.format( e ) )
            raise

    def get_cart_products( self, client_id  ):
        ''' Used for Unit Testing.
            Get the products that are in the shopping cart.
        '''        
        try:
            '''key    = self.keySchemaInv.get_inventory_key( cocedis_id, product_id )'''
            key = 'cart:client:{}' .format( client_id )
            result = self.get_cart_products_lua( keys = [key], args = [ self.REDIS_DB ] )
            print( result )
            print( '...' )
            
        except Exception as e:
            print( 'Cart.get_items_qty(), error: {}'.format( e ) )
            raise



    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, override_quantity=False, cocedis_id = 0 ):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'cocedis_id': cocedis_id,
                'quantity'  : 0,
                'price'     : str(product.price),

                'width'         : product.width ,
                'height'        : product.height ,
                'length'        : product.length ,
                'weight'        : product.weight ,
                'mass_unit'     : product.mass_unit ,
                'distance_unit' : product.distance_unit ,
            }

        if override_quantity:
            #todo: inventory reserve or take back items
            self.cart[product_id]['quantity'] = quantity
            
        else:
            self.cart[product_id]['quantity'] += quantity
            #todo: inventory reserve item

        self.save()
        


    def __init__(self, params=None ) -> None:
        self.lua_dir      = '/home/art/git/redis/cart/lua'
        self.keySchemaCart = KeySchemaCart()

        self.connect( )

        # register lua scripts
        self.del_keys_lua      = self.register_lua_script( 'del_keys.lua' )
        
        self.get_cart_items_lua     = self.register_lua_script( 'get_cart_items.lua' )
        self.get_cart_items_qty_lua = self.register_lua_script( 'get_cart_items_qty.lua' )
        self.get_cart_products_lua  = self.register_lua_script( 'get_cart_products.lua' )

        self.cart = {}
        # self.cart = get cart items from redis





