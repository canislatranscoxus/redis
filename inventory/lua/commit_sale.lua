--[[
description:    this script update the inventory when user commit sale of
                one cocedis - one product_id - a quantity of items


                key, must specify Distribution Point and product_id, in the next format
                    inv:dp:<cocedis_id>:product:<product_id>

                quantity, the number of items

                return if transaction was completed, True or false.
--]]

local key, db, quantity = KEYS[1], tonumber( ARGV[1] ), tonumber( ARGV[2] )
local reserved = 0
local completed = false

redis.call( "select", db )
reserved = tonumber( redis.call( "HGET", key, 'reserved' ) )

if reserved >= quantity then
    redis.call( 'HINCRBY', key, 'reserved', -quantity )
    redis.call( 'HINCRBY', key, 'total'   , -quantity )
    completed = true
end 

return completed