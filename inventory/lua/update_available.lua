--[[
description:    this script add available items when 
                a Distribution Point receives new merchandise. 

                key, must specify Distribution Point and product_id, in the next format
                    inv:dp:<cocedis_id>:product:<product_id>

                quantity, the number of items client are puting in the shoping cart

                return if transaction was completed, True or false.
--]]

local key, db, quantity = KEYS[1], tonumber( ARGV[1] ), tonumber( ARGV[2] )
local available = 0
local completed = false

redis.call( "select", db )
redis.call( 'HSET', key, 'available', quantity )
completed = true

return completed