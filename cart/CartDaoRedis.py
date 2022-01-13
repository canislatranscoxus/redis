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
from typing import ItemsView, Mapping
import redis

from DaoRedis       import DaoRedis
from KeySchemaCart  import KeySchemaCart


num_of_cocedis  = 6
num_of_products = 31

class CartDaoRedis ( DaoRedis ):

    cart                   = None
    ItemsView              = None
    keySchemaCart          = None
    del_keys_lua           = None
    get_cart_items_lua     = None    
    get_cart_product_qty_lua = None
    get_cart_products_lua  = None

    REDIS_HOST      = None 
    REDIS_PORT      = None
    REDIS_DB        = None
    REDIS_AUTH      = None



    def format_cart_items( self, row_list ):
        '''Format the cart items,
        input : result from redis. Row list with product_id and quantity.
        output: dictionary of dictionary'''
        try:
            #
            d = {}
            for i in range( 0, len(row_list), 2  ):
                item = { 
                    'quantity' : row_list[ i + 1 ]
                 }
                product_id = row_list[ i ]
                d[ product_id ] = item
            
            return d

        except Exception as e:
            print( 'CartDaoRedis.product_qty_2_dic(), error: {}'.format( e ) )
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
            print( 'CartDaoRedis.product_qty_2_dic(), error: {}'.format( e ) )
            raise

    def format_found_products( self, row_list ):
        '''Take as input the found products from redis and 
        return as output the products data as a dictionary, where 
                key   is product_id, and
                value is a dictionary with product data'''

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
            print( 'CartDaoRedis.product_qty_2_dic(), error: {}'.format( e ) )
            raise

    def get_cart_items( self, client_id  ):
        '''get the cart items from redis, brings product_id and quantity for each item.'''
        try:
            key = 'cart:client:{}' .format( client_id )
            result = self.get_cart_items_lua( keys = [key], args = [ self.REDIS_DB ] )

            if  result      == None or len( result ) == 0 or    \
                result[ 0 ] == None or len( result[ 0 ] ) == 0 :
                self.cart = {}
                return self.cart

            self.cart = self.format_cart_items( result[ 0 ] )
            products  = self.format_found_products( result[ 1 ] )

            for product_id, item in self.cart.items():
                item[ 'product' ] = products[ product_id ]
            
            return self.cart

        except Exception as e:
            print( 'CartDaoRedis.get_items_qty(), error: {}'.format( e ) )
            raise

    def get_product_qty( self, client_id  ):
        ''' Used for Unit Testing.
            Get product_id and qty, for all the cart items.
        '''
        try:
            '''key    = self.keySchemaInv.get_inventory_key( cocedis_id, product_id )'''
            key = 'cart:client:{}' .format( client_id )
            result = self.get_cart_product_qty_lua( keys = [key], args = [ self.REDIS_DB ] )
            #print( result )
            return result
            
        except Exception as e:
            print( 'CartDaoRedis.get_items_qty(), error: {}'.format( e ) )
            raise

    def get_cart_products( self, client_id  ):
        ''' Used for Unit Testing.
            Get the products that are in the shopping cart.
        '''        
        try:
            '''key    = self.keySchemaInv.get_inventory_key( cocedis_id, product_id )'''
            key = 'cart:client:{}' .format( client_id )
            result = self.get_cart_products_lua( keys = [key], args = [ self.REDIS_DB ] )
            return result
            
        except Exception as e:
            print( 'CartDaoRedis.get_items_qty(), error: {}'.format( e ) )
            raise

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum( item['quantity'] for item in self.cart.values() )

    def add(self, client_id, product_id, quantity=1, override_quantity=False ):
        """
        Add a product to the cart or update its quantity.
        """
        try:
            key = self.keySchemaCart.get_cart_key( client_id )

            if override_quantity:
                self.conn.hset   ( key, product_id, quantity )
            else:
                self.conn.hincrby( key, product_id, quantity )

        except Exception as e:
            print( 'CartDaoRedis.add(), error: {}'.format( e ) )
            raise        

    def remove(self, client_id, product_id ):
        """
        Add a product to the cart or update its quantity.
        """
        try:
            
            key = self.keySchemaCart.get_cart_key( client_id )
            self.conn.hdel( key, product_id )

        except Exception as e:
            print( 'CartDaoRedis.add(), error: {}'.format( e ) )
            raise        

    def clear(self, client_id ):
        # remove all items in cart, and cart from session.
        try:
            key = self.keySchemaCart.get_cart_key( client_id )
            self.conn.delete( key )
            self.items.clear()

        except Exception as e:
            print( 'CartDaoRedis.clear(), error: {}'.format( e ) )
            raise



    def __init__(self, params=None ) -> None:
        try:
            self.lua_dir      = '/home/art/git/redis/cart/lua'
            self.keySchemaCart = KeySchemaCart()

            self.connect( )

            # register lua scripts
            self.del_keys_lua      = self.register_lua_script( 'del_keys.lua' )
            
            self.get_cart_items_lua       = self.register_lua_script( 'get_cart_items.lua' )
            self.get_cart_product_qty_lua = self.register_lua_script( 'get_cart_product_qty.lua' )
            self.get_cart_products_lua    = self.register_lua_script( 'get_cart_products.lua' )

            self.cart = {}
            # self.cart = get cart items from redis

        except Exception as e:
            print( 'CartDaoRedis.__init__(), error: {}'.format( e ) )
            raise        




