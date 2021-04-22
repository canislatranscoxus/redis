--[[
    Create one new sorted set per each term that 
    will contain the tf-idf of the term for all the products.


                               N 
    tf-idf( t, d ) =  TF * ----------
                              DF
    
    t  = term. Word.
    d  = document. Product
    N  = Number of documents in Corpus. How many products.
    DF = Document Frequency. In how many documents the term occur.  

    Input:
        key : the key of the new DF sorted set.
        args:   
                database = the number of the database. 
                pattern  = the pattern to find the tf keys.
                tf_idf_prefix =  the prefix to create name of the tf_idf keys.

    Output: A new sorted set with TF-DFsvper each term.
]]
local df_key         = KEYS[1]
local db, pattern, n, tf_idf_prefix = tonumber( ARGV[1] ), ARGV[2], tonumber( ARGV[3] ), ARGV[4]
local cur1, cur2     = 0, 0
local word
local scan1, scan2
local tf, df, tf_idf = 0, 0, 0
local idf = 0
local tmp = 0
local res = 0
local tf_prefix, tf_idf_key, product_id


redis.call( "select", db )

tf_prefix = string.gsub( pattern, "*", "" )

repeat
    -- get token keys with TF 
    scan1 = redis.call('SCAN', cur1, 'MATCH', pattern )
    for i, tf_key in ipairs( scan1[2] ) do

        word = string.gsub( tf_key, tf_prefix, "" )
        df   = redis.call( 'HGET', df_key, word )

        print( string.format( 'tf_key: %s', tf_key ) )
        print( string.format( 'word  : %s', word ) )

        -- loop in the sorted set
        repeat
            scan2 = redis.call('ZSCAN', tf_key, cur2  )
            for i, v in ipairs( scan2[2] ) do
                --redis.call( 'DEL', v )
        
                res = tonumber( i ) % 2
                if res == 0 then

                    print( '--------------------------- \n')

                    tf     = tonumber  ( v )
                    idf    = math.log10( n / df )
                    tf_idf = tf * math.log10( n / df )

                    tmp = n / df

                    print( string.format( 'tf  = %.4f', tf  ))
                    print( string.format( 'df  = %.4f', df  ))
                    
                    print( string.format( 'idf = %.4f', idf ))
                    print( string.format( 'tmp = %.4f', tmp ))

                    tf_idf_key = tf_idf_prefix .. word

                    print( string.format( '\n product_id = %s' , product_id ) )
                    print( string.format( 'tf_idf_key = %s ', tf_idf_key ) )
                    print( string.format( 'tf_idf = %.4f'   , tf_idf     ) )
                    

                    redis.call('ZADD', tf_idf_key, tf_idf, product_id  )
                else
                    product_id = v
                end
            end
            cur2 = tonumber( scan2[1] )
        until ( cur2 == 0 )


    end
    cur1 = tonumber( scan1[1] )
until ( cur1 == 0 )
