local db = tonumber( ARGV[1] )
local result
local a
local delta = 0.10

redis.call( "select", db )

print(_VERSION)
print( 'playing with maths' )

result = math.log( 1.0 )
print( 'log( 1.0 )' )
print( result )

for i = 0,1,0.10 
do 
    result = math.log10( i )
    print( string.format( 'log( %.4f ) = %.4f ', i, result ) )
    
end


a = math.rad( result )
print( a )

return result