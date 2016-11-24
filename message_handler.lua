
--[[
-- keys[1]: type:id
-- keys[2]: id
-- keys[3]: message
-- KEYS[4]: name
]]--

local rank_key = "rank:" .. KEYS[1] 
local message_key = "message:" .. KEYS[1] .. ":" .. KEYS[2]
redis.call('zincrby', rank_key, 1, KEYS[2])
redis.call('rpush', message_key, KEYS[3])
redis.call('hset', 'user_name', KEYS[2], KEYS[4])

return 'ok'

