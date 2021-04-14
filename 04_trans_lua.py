import redis
import os
import sys

REDIS_HOST = os.environ[ 'REDIS_HOST' ]
REDIS_PORT = os.environ[ 'REDIS_PORT' ]
#REDIS_DB   = os.environ[ 'REDIS_DB'   ]
REDIS_DB   = 10
REDIS_AUTH = os.environ[ 'REDIS_AUTH' ]


# connect to redis
redis = redis.Redis( host     = REDIS_HOST
                ,port     = REDIS_PORT
                ,db       = REDIS_DB
                #,password = REDIS_AUTH
                ,decode_responses= True
                )


# KEYS[1] A key holding a numeric value
# KEYS[2] A second key holding a numeric value
# ARGV[1] A string naming the operation to be performed. Valid
#         values are "max" and "sum"
# Returns the result of the operation (max or sum).
stats_script = """
    -- Convert arguments to numbers
    local k1 = redis.call('get', KEYS[1])
    local k2 = redis.call('get', KEYS[2])
    if ARGV[1] == "sum" then
      return k1 + k2
    elseif ARGV[1] == "max" then
      return math.max(k1, k2)
    else
      return nil
    end
"""

def main():

    redis.set("hits:homepage", 2000)
    redis.set("hits:loginpage", 75)

    homepage  = redis.get( "hits:homepage"  )
    loginpage = redis.get( "hits:loginpage" )

    # Register our script with the Redis Python client and
    # return a callable object for invoking our script.
    stats = redis.register_script(stats_script)

    # Invoke our "sum" script.
    # This calls SCRIPT LOAD and then stores
    # the SHA1 digest of the script for future use.
    total = stats(["hits:homepage", "hits:loginpage"], ["sum"])
    assert(total == 2075)

    # Two more tests.
    max = stats(["hits:homepage", "hits:loginpage"], ["max"])
    assert(max == 2000)

    print( 'calling script to sum {} + {} = {}'.format( homepage, loginpage, total ) )
    print( 'calling script get max {} or {} ? {}'.format( homepage, loginpage, max ) )

if __name__ == "__main__":
    main()