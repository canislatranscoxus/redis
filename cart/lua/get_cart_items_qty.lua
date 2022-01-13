--[[
description:    this script take as input a cart key, and
                as output return the items and quantities from the shopping cart.
                The shoping cart is a Hash in Redis.

--]]

local key, db  = KEYS[1], tonumber( ARGV[1] ) 
local h = {}

redis.call( "select", db )
h = redis.call( 'HGETALL', key )

return h