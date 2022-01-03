--[[
description:    this script reserve items when shoping. 
                It is when client take some items and put them in the shopping cart.

                key, must specify Distribution Point and product_id, in the next format
                    inv:dp:<cocedis_id>:product:<product_id>

                quantity, the number of items client are puting in the shoping cart

                return if transaction was completed, True or false.
--]]

local key, db, quantity = KEYS[1], tonumber( ARGV[1] ), tonumber( ARGV[2] )
local available = 0
local completed = false

redis.call( "select", db )
available = tonumber( redis.call( "HGET", key, 'available' ) )

if available >= quantity then
    redis.call( 'HINCRBY', key, 'available', -quantity )
    redis.call( 'HINCRBY', key, 'reserved' ,  quantity )
    completed = true
end 

return completed