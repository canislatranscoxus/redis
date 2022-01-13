--[[
description:    this script take as input a cart key, and
                as output return products that are in the shopping cart.
                The result is a list from Redis.
                
               fisrt element - Number of products found
               next we have the data in the pattern

               element - attribute
               element - value
               element - attribute
               element - value
               ...
--]]

local key, db  = KEYS[1], tonumber( ARGV[1] ) 

-- get product_id and quantity 
local product_qty = {}
redis.call( "select", db )
product_qty = redis.call( 'HGETALL', key )


local products = {}
local product_ids = {}
local ids = ""

redis.call( "select", db )
product_ids = redis.call( 'HKEYS', key )

-- convert product_ids list to string
for index, value in pairs( product_ids ) do
   print( value )

   if string.len( ids ) > 0 then
    ids = ids .. "|"
   end
   ids = ids  .. "@id:" .. value
end

products =  redis.call( 'FT.SEARCH', 'es_product_idx', ids )


return products