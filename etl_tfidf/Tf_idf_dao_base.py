import abc

class Tf_idf_dao_base( abc.ABC ):

    @abc.abstractmethod
    def clean_previous_etl( self ):
        pass

    @abc.abstractmethod
    def insert_tf( self, product_id, tfs, pipeline ):
        '''insert the tf in the sorted set key, using mapping

        :param string product_id: the id of the product. 
        :param json product: A dictionary that contains how many times the words occur. 
        '''
        pass

    @abc.abstractmethod
    def count_df( self ):
        pass

    @abc.abstractmethod
    def count_tf_idf( self, num_of_products ):        
        pass
