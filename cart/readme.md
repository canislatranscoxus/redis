# Shopping cart

This is a Shopping Cart implemented using python and Redis.
The cart of each client is stored in redis in a hash 
that contains product_id and quantity.

## Cart data structure in redis

Cart is a Hash ( dictionary )

cart:client: < client_id >
{
  '<product_id>' : 'quantity',
  '<product_id>' : 'quantity', 
  '<product_id>' : 'quantity', 
    .
    .
    .      
}


## Add Update items to cart

we add to the car, for 
  client_id  =  1, 
  product_id = 24
  quantity   =  1

command:
```
hset cart:client: <client_id> <product_id> <quantity>
```

example:
``` 
hset cart:client:1 24 1
hset cart:client:1 17 2
```

## See cart items and quantity

command:
```
hgetall cart:client:<client_id>
```

example:
```
hgetall cart:client:1
```


## Get Products using our cart

here we execute two steps

 * get product_id of each cart item. (cart keys)
 * get products documents( FTS, Full Text Search  )

Redis Command to get the product IDs of the cart items
```
hkeys cart:client:< client_id >
``` 

Redis Command to search the products
```
FT.SEARCH es_product_idx "@id:<product_id> | @id: ..."
```

example:
```
FT.SEARCH es_product_idx "@id:24 | @id:17"
```

## Get total to pay
Form python call a lua script that returns
 cart list and products
in python calculate the totals 


