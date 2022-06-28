--[[
description:    take as input a key, database and dictionary and insert that to redis.
--]]


local key, db, my_dic = KEYS[1], tonumber( ARGV[1] ), cjson.decode( ARGV[2] )

redis.call( "select", db )

for field, value in pairs( my_dic ) do
    print( field, ': ' , value  )
    redis.call( "HSET",  key, field, value )
end


