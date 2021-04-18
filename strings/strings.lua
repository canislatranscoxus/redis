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

-- insert 3 k v to sorted set music.
redis.call( 'ZADD', 'music', 3, 'guitar' )
redis.call( 'ZADD', 'music', 1, 'flute' )
redis.call( 'ZADD', 'music', 2, 'sax' )


return result