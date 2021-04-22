local db, pattern = tonumber( ARGV[1] ), ARGV[2]
local cur = 0
local scan
redis.call( "select", db )

repeat
    scan = redis.call('SCAN', cur, 'MATCH', pattern )
    for i, v in ipairs( scan[2] ) do
        redis.call( 'DEL', v )
    end
    cur = tonumber( scan[1] )
until ( cur == 0 )

return scan