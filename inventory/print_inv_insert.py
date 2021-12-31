'''
description: Inventory Strategy 3. One hash per Cocedis and product.
             This is simplest and fastest.
             And other user will not be waiting while they buy other products.


            This script connect to  Redis and set the inventaory of All cocedis.
             We specify the amount of total, available, reserved, allocated values per each product.


To delete this keys in redis use the command below 

del inv_cocedis:1 inv_cocedis:2 inv_cocedis:3 inv_cocedis:4 inv_cocedis:5 inv_cocedis:6

'''

num_of_cocedis  = 6
num_of_products = 31

d = {
    'cocedis_id' : 0,
    'product_id' : 0,
    'total'      : 5,
    'available'  : 3,
    'reserved'   : 1,
    'allocated'  : 1,
    }

s = '''HSET inv:dp:{cocedis_id}:product:{product_id} total {total} available {available} reserved {reserved} allocated {allocated}'''

#s = 'HSET inv:dp:{}:product:{} total: 5 available 3 reserved 1 allocated 1'


for cocedis_id in range( 0, num_of_cocedis + 1 ):
    for product_id in range( 1, num_of_products + 1 ):

        d[ 'cocedis_id' ] = cocedis_id
        d[ 'product_id' ] = product_id
        cmd               = s.format( **d )
        print( cmd )