--[[
description:    this script take back items when shoping. 
                It is when client take back from shopping cart to shelf.

                key, must specify Distribution Point and product_id, in the next format
                    inv:dp:<cocedis_id>:product:<product_id>

                quantity, the number of items client are taking back in theshelf

                return if transaction was completed, True or false.
--]]

local key, db, quantity = KEYS[1], tonumber( ARGV[1] ), tonumber( ARGV[2] )
local reserved = 0
local completed = false

redis.call( "select", db )
reserved = tonumber( redis.call( "HGET", key, 'reserved' ) )

if reserved >= quantity then
    redis.call( 'HINCRBY', key, 'reserved' , -quantity )
    redis.call( 'HINCRBY', key, 'total' , -quantity )    
    completed = true
end 

return completed