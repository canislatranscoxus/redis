'''
Description: create redis queries based on SQL queries.
'''

# ------------------------------------------------------------------------------
# SELECT *
# FROM table_idx
# WHERE num_field IN ( list_of_values )


num_field = 'product_id'
list_of_values = [ 2, 4, 6 ]
q = ''

a = map( lambda value: ' @{num_field}:[ {value} {value} ]'.format(num_field=num_field, value=value)
         , list_of_values )
q = ' | '.join( a )
print( 'redis query: {}'.format( q ) )


# ------------------------------------------------------------------------------
# SELECT *
# FROM table_idx
# WHERE num_field IN ( list_of_values )
#
# in 1 line

num_field = 'client_id'
values = [ 3, 5, 7 ]
q = ''

q = ' | '.join( map( lambda v: ' @{num_field}:[ {v} {v} ]'.format(num_field=num_field, v=v), values ) )

print( 'redis query: {}'.format( q ) )

