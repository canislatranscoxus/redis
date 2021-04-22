--[[
    Create one new sorted set with the Document Frequencies (DFs) of all the terms.
    If a previous DFs sorted set exist, it is deleted.
    
    Input:
        key : the key of the new DF sorted set.
        args: database, and pattern of the TF sorted sets. 

    Output: A new sorted set with DFs.
]]

local df_key, db, pattern = KEYS[1], tonumber( ARGV[1] ), ARGV[2]
local cur, num_docs = 0, 0
local word
local scan
local res = 0


redis.call( "select", db )

print( pattern )
print( 'Count_df.lua, words found:' )


repeat
    scan = redis.call('SCAN', cur, 'MATCH', pattern )

    for i, tf_key in ipairs( scan[2] ) do

        print( 'key', tf_key )

        num_docs = redis.call( 'ZCOUNT', tf_key, '-inf', '+inf' )
        word     = string.gsub( tf_key, pattern, "")

        print( word, ', num of docs:  ', num_docs )

        redis.call( 'HSET', df_key, word, num_docs )

        
    end
    cur = tonumber( scan[1] )
until ( cur == 0 )

return 0

