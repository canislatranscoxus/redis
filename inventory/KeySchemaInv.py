DEFAULT_KEY_PREFIX = 'inventory'

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



class KeySchemaInv:

    prefix = DEFAULT_KEY_PREFIX


    def __init__(self, prefix: str = DEFAULT_KEY_PREFIX):
        self.prefix = prefix

    @prefixed_key
    def get_inventory_key(self, cocedis_id, product_id ):
        key = f'{cocedis_id}:{product_id}'
        return key      


    @prefixed_key
    def get_prefix(self, cocedis_id ):
        
        key = ''
        if cocedis_id != None:
            key = f'{cocedis_id}:'

        return key        

