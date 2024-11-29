import json
import sys
import redis
import redis.commands.search
import redis.commands.search
import redis.commands.search.aggregation as aggs
import redis.commands.search.reducers as reducers
from   redis.commands.search.query  import NumericFilter, Query

class Cool_class:

    def select_order(self, client_id ):
        # Get the last 10 orders of the client. Only order, no items. See sql
        #
        # SELECT *
        # FROM my_order_index
        # WHERE client_id =   <client_id>
        # and row_num between offset and (offset + num)
        # SORT BY order_id DESC
        # LIMIT 10
        try:
            offset = 0
            num    = 10
            q      = '@client_id:[ {client_id} {client_id} ]'.format(client_id=client_id)
            query  = (Query( q ).return_fields( 'order_id', 'client_id', 'paid' )
                      .paging(offset, num).sort_by( 'order_id' , asc=False))

            # query = (Query(q).return_fields(  )
            #          .paging(offset, num).sort_by('order_id', asc=False))

            orders = self.search( query )
            return orders
        except Exception as e:
            print( 'OrderDaoRedis.select_orders(), error: {}'.format(e) )
