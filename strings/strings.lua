local key1, key2  = KEYS[1], KEYS[2]
local db, pattern = tonumber( ARGV[1] ), ARGV[2]
local cur = 0
local scan
local result

redis.call( "select", db )

print( key1 )
print( key2 )

result = string.gsub( key1, pattern, "")
print( result )

result = string.gsub( key2, pattern, "")
print( result )


return result