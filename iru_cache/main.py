from collections import OrderedDict
import time


class LRUCache:
    def __init__(self, capacity: int, ttl: int):
        """初始化缓存，设置容量和TTL（秒）"""
        self.cache = OrderedDict()
        self.capacity = capacity
        self.ttl = ttl

    def get(self, key: str):
        """获取缓存值，若过期或不存在返回None"""
        if key in self.cache:
            if time.time() - self.cache[key]['timestamp'] < self.ttl:
                self.cache.move_to_end(key)  # 更新为最近使用
                return self.cache[key]['value']
            else:
                del self.cache[key]  # 删除过期条目
        return None

    def put(self, key: str, value: any):
        """存入缓存值，超出容量时淘汰最久未使用的条目"""
        if key in self.cache:
            del self.cache[key]
        self.cache[key] = {'value': value, 'timestamp': time.time()}
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # 移除最老的条目

    def invalidate(self, key: str):
        """手动失效指定缓存条目"""
        if key in self.cache:
            del self.cache[key]


# 示例使用
if __name__ == "__main__":
    cache = LRUCache(capacity=100, ttl=3600)  # 容量100，TTL 1小时
    cache.put('product_123', {'name': 'Product 123', 'price': 19.99})

    # 设置睡眠时长
    # time.sleep(2)
    product = cache.get('product_123')
    if product:
        print(f"缓存命中: {product}")
    else:
        print("缓存未命中，需从数据库获取")
    cache.invalidate('product_123')  # 手动失效
    print(f"失效后获取: {cache.get('product_123')}")
