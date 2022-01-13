--[[
description:    this script execute 2 steps. 
                One step is get cart items and quantities.
                Second step, get products.
--]]

local key, db  = KEYS[1], tonumber( ARGV[1] ) 


local result = { }


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

result = {
    [ "product_qty"] = product_qty,
    [ "products"   ] = products
}


return 'result'
