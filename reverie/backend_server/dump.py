import redis
import json

# 连接到Redis数据库
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# 设置示例数据
r.hset('run', 'first_name', 'Peter')

# 获取所有键
keys = r.keys('*')

# 创建一个字典来存储所有键的结果
all_data = {}
location_data = {}
# 遍历所有键并获取它们的值
for key in keys:
    result = r.hgetall(key)
    if "location" not in key:
        
        all_data[key] = result
    else:
        location_data[key] = result

# 将结果写入文件
with open('llm_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

with open('location_data.json', 'w', encoding='utf-8') as f:
    json.dump(location_data, f, ensure_ascii=False, indent=4)


