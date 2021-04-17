local key, db = KEYS[1], tonumber( ARGV[1] )

redis.call( "select", db )
local n

n = redis.call( 'ZCOUNT', key, '-inf', '+inf' )

return n
