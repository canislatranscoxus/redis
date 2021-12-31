DEFAULT_KEY_PREFIX = 'search_box'

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
    def get_tf_key(self, language, token = '' ):
        key = f'{language}:tf:{token}'
        return key

    @prefixed_key
    def get_df_key(self, language ):
        key = f'{language}:df'
        return key      

    @prefixed_key
    def get_tf_idf_key(self, language, token = '' ):
        key = f'{language}:tf_idf:{token}'
        return key

    @prefixed_key
    def get_prefix(self, language ):
        key = f'{language}'
        return key        

