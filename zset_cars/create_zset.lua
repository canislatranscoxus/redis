local src_key, tar_key, db = KEYS[1], KEYS[2], tonumber( ARGV[1] )
local cur, n, speed        = 0, 0, 0
local car
local scan
local res = 0


redis.call( "select", db )
n = redis.call( 'ZCOUNT', src_key, '-inf', '+inf' )


print( '\n\n number of elements of' )
print( src_key )
print( n )

print( 'zscan for src_key ... begin' )

repeat
    scan = redis.call('ZSCAN', src_key, cur  )
    for i, v in ipairs( scan[2] ) do
        print( v )
        
        res = tonumber( i ) % 2
        if res == 0 then
            speed = tonumber( v )
            redis.call('ZADD', tar_key, speed, car  )
        else
            car = v
        end

    end
    cur = tonumber( scan[1] )
until ( cur == 0 )
return src_key

