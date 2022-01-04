--[[
Lua is not accepting Array parameters

description:    this script update the inventory when user commit sale of
                all the items in the cart


                key, must specify Distribution Point and product_id, in the next format
                    inv:dp:<cocedis_id>:product:<product_id>

                quantity, the number of items

                return if transaction was completed, True or false.
--]]

local db, rows = tonumber( ARGV[1] ), ARGV
local key = ""
local reserved = 0
local quantity = 0
local completed = false

redis.call( "select", db )

for index, row in ipairs( rows ) do

    key      = "inv:dp:" .. row[ "cocedis_id" ] .. ":product:" .. row[ "product_id" ]
    reserved = tonumber( redis.call( "HGET", key, 'reserved' ) )
    quantity = tonumber( row[ "quantity" ] )

    if reserved >= quantity then
        redis.call( 'HINCRBY', key, 'reserved' , -quantity )
        redis.call( 'HINCRBY', key, 'total' , -quantity )    
        completed = true
    end 

end



return completed