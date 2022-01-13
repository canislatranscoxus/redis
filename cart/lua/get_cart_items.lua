--[[
description:    this script execute 2 steps. 
                One step is get cart items and quantities.
                Second step, get products.
--]]

local key, db  = KEYS[1], tonumber( ARGV[1] ) 


-- get product_id and quantity 
local product_qty   = {}
local products      = {}
local product_ids   = {}
local ids           = ""

redis.call( "select", db )
product_qty = redis.call( 'HGETALL', key )


-- convert product_ids list to string
redis.call( "select", db )
product_ids = redis.call( 'HKEYS', key )

for index, value in pairs( product_ids ) do
   print( value )

   if string.len( ids ) > 0 then
    ids = ids .. "|"
   end
   ids = ids  .. "@id:" .. value
end

-- get products
products =  redis.call( 'FT.SEARCH', 'es_product_idx', ids )

-- pack results in an array
local result = { product_qty, products}

return result
