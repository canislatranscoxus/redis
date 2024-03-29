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
    def reserve( self, cocedis_id, product_id, quantity ):
        '''Take a quantity of products from available and put them in reserved,
        in he inventory'''
        pass

    @abc.abstractmethod
    def take_back( self, cocedis_id, product_id, quantity ):
        pass

    @abc.abstractmethod
    def commit_sale( self, cocedis_id, product_id, quantity ):
        pass


    @abc.abstractmethod
    def add_available( self, cocedis_id, product_id, quantity ):
        '''Add items in One cocedis. This method must be called when a
        Distribution Point receive products.

        cocedis_id : int. 
         '''
        pass


    @abc.abstractmethod
    def update_available( self, cocedis_id, product_id, quantity ):
        '''Update items to the inventory of One cocedis. This method must be called when a
        Distribution Point is starting, or need to update their real inventory. 
        For example, every week update the real data.

        cocedis_id : int. 
         '''
        pass



    @abc.abstractmethod
    def mock_data( self  ):
        '''Initialize the inventory with mocked data, dummy data.'''
        pass
