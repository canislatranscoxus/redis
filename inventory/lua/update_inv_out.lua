--[[
description:    update the inventory when product go out of warehouse.

    

    db  : it represent the database. The correct value is cero.

    id_qty: A string of a json with product_id and quantity.



sample data
 
hset inventory:x:1 onhand    150
hset inventory:x:1 available 140
hset inventory:x:1 reserved   10
hset inventory:x:1 allocated   0

hset inventory:x:2 onhand    150
hset inventory:x:2 available 140
hset inventory:x:2 reserved   10
hset inventory:x:2 allocated   0


--]]

local db, supplier_id, id_qty = tonumber( ARGV[1] ), ARGV[2], cjson.decode( ARGV[3] )

-- key : is the hash key for a warehouse product. the key has this layout
--            inventory:<supplier_id>:<product_id>
local key, d

-- ----------------------------------------------------------------------------
-- UDF table ( User Defined Functions )
-- ----------------------------------------------------------------------------
local udf           = {}

-- ----------------------------------------------------------------------------
-- log messages to redis

local function logit2( msg )
    --- RPUSH log:aat "hello"
    redis.call( 'RPUSH', 'log:aat',  msg )
end

-- ----------------------------------------------------------------------------
-- get stock levels of a cocedis product in an array.
function udf.get_stock_levels( key )
    local a
    a = redis.call( 'HGETALL', key )
    return a
end

-- ----------------------------------------------------------------------------

function udf.array_to_dict( a )
    local dict = {} -- dictionary
    local n
    local k
    local v

    -- size of the array.
    n = #a -1

    for i = 1, n, 2   do
        k = a[ i ]
        v = tonumber( a[ i + 1 ] )
        dict[ k ] = v
    end

    --logit( 'dict size: ' .. #dict )

    return dict
end


-- ----------------------------------------------------------------------------

function udf.run( db, supplier_id, id_qty )

    local key
    local a
    local d = {} -- dictionary

    redis.call( "select", db )

    logit2( 'run() ... begin' )

    for id, qty in pairs( id_qty ) do
        
        key = 'inventory:' .. supplier_id .. ':' .. id


        logit2( 'key  ' .. key )

        a   = udf.get_stock_levels( key )
        d   = udf.array_to_dict( a )

        d[ 'onhand'    ] = d[ 'onhand'    ] - qty 
        d[ 'reserved'  ] = d[ 'reserved'  ] - qty 
        --d[ 'available' ] = 
        --d[ 'allocated' ] = 

        redis.call( "HSET",  key, 'onhand'   , d[ 'onhand'    ] )
        redis.call( "HSET",  key, 'reserved' , d[ 'reserved'  ] )
        --redis.call( "HSET",  key, 'available', value )
        --redis.call( "HSET",  key, 'allocated', value )

    end
    
    logit2( 'run() ... end' )

    return 0
end

-- ----------------------------------------------------------------------------
-- main
-- ----------------------------------------------------------------------------

redis.call( 'DEL', 'log:aat' )

local status, result = pcall( udf.run, db, supplier_id, id_qty )

local a = { result, status  }
return a