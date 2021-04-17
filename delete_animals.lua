local db, cur, pattern = tonumber( ARGV[1] ), tonumber( ARGV[2] ), ARGV[3]

redis.call( "select", db )
local scan

repeat
    scan = redis.call('SCAN', cur, 'MATCH', pattern )
    for i, v in ipairs( scan[2] ) do
        redis.call( 'DEL', v )
    end
    cur = tonumber( scan[1] )
until ( cur == 0 )

return scan

