'''
Description: create redis queries based on SQL queries.
'''

# SELECT *
# FROM table_idx
# WHERE num_field IN ( list_of_values )


num_field = 'product_id'
list_of_values = [ 2, 4, 6 ]
q = ''

for value in list_of_values :
    s = ' @{num_field}:[ {value} {value} ]'.format( num_field = num_field, value = value )
    if q == '':
        q = q + s
    else:
        q = q + ' | ' + s

print( 'redis query: {}'.format( q ) )


