'''
description: Inventory Strategy 2. One hash per Cocedis.
             Less complex than having all the inventory of the stores in one table.
             But still complex, and other user will be waiting ....   


            This script create a Redis command to add or update the inventaory of One cocedis.
             We specify the amount of total, available, reserved, allocated values per each product.


To delete this keys in redis use the command below 

del inv_cocedis:1 inv_cocedis:2 inv_cocedis:3 inv_cocedis:4 inv_cocedis:5 inv_cocedis:6

'''

cocedis_id      = 1
num_of_products = 31

txt = 'HSET inv_cocedis:{}'.format( cocedis_id )
s = 'total:{i} 5 available:{i} 3 reserved:{i} 1 allocated:{i} 1 '
a = []
a.append( txt )

print( txt )

for i in range( 1, num_of_products + 1 ):
    row = s.format( i=i )
    a.append( i )
    print( row )