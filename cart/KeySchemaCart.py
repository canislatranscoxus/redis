DEFAULT_KEY_PREFIX = 'cart'

def prefixed_key(f):
    """
    A method decorator that prefixes return values.

    Prefixes any string that the decorated method `f` returns with the value of
    the `prefix` attribute on the owner object `self`.
    """
    def prefixed_method(self, *args, **kwargs):
        key = f(self, *args, **kwargs)
        return f"{self.prefix}:{key}"

    return prefixed_method



class KeySchemaCart:

    prefix = DEFAULT_KEY_PREFIX


    def __init__(self, prefix: str = DEFAULT_KEY_PREFIX):
        self.prefix = prefix

    @prefixed_key
    def get_cart_key(self, client_id ):
        key = f'client:{client_id}'
        return key      

    def get_search_box_key(self, language_code ):
        key = f'{language_code}_product_idx'
        return key

    def get_product_id_from_search_box_key( self, key ):
        # example:  key = 'search_box:es:17'
        product_id = key[ 14: ]
        return product_id

    @prefixed_key
    def get_prefix(self, cocedis_id ):
        
        key = ''
        if cocedis_id != None:
            key = f'dp:{cocedis_id}:'

        return key        

