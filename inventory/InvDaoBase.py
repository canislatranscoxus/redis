'''
Description: This class is used to Connect to Redis an execute the operations
             to handle the Inventory.

            We use the word "cocedis" to refer a "Distribution Point", sometime "dp".

'''

import os
import redis

import abc

class InvDaoBase( abc.ABC ):

    conn = None

    @abc.abstractmethod
    def connect( self, params ):
        pass

    @abc.abstractmethod
    def del_inventory( self, cocedis_id = None ):
        pass


    @abc.abstractmethod
    def reserve_item( self, cocedis_id, product_id, quantity ):
        '''Take a quantity of products from available and put them in reserved,
        in he inventory'''
        pass

    @abc.abstractmethod
    def take_back_item( self, cocedis_idis, product_id, quantity ):
        pass


    @abc.abstractmethod
    def add_update_cocedis( self, cocedis_id, product_inv_list ):
        '''Add or update the inventory of One cocedis. This method must be called when a
        Distribution Point is starting, or need to update their real inventory.

        cocedis_id : int. 
         '''
        pass

    @abc.abstractmethod
    def mock_data( self  ):
        '''Initialize the inventory with mocked data, dummy data.'''
        pass
