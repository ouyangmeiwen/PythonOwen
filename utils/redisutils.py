import redis
from typing import Any, List, Optional, Union
import time

class RedisClient:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0, password: Optional[str] = None):
        # 初始化 Redis 连接，支持密码认证
        self.client = redis.StrictRedis(host=host, port=port, db=db, password=password, decode_responses=True)

    # 字符串类型操作
    def set_string(self, key: str, value: str, expire_time: Optional[int] = None) -> bool:
        """设置字符串值，并可指定过期时间（秒）"""
        result = self.client.set(key, value)
        if expire_time:
            self.client.expire(key, expire_time)
        return result

    def get_string(self, key: str) -> Optional[str]:
        """获取字符串值"""
        return self.client.get(key)

    # 哈希类型操作
    def set_hash(self, key: str, field: str, value: Any, expire_time: Optional[int] = None) -> bool:
        """设置哈希表中的字段值，并可指定过期时间"""
        result = self.client.hset(key, field, value)
        if expire_time:
            self.client.expire(key, expire_time)
        return result

    def get_hash(self, key: str, field: str) -> Optional[str]:
        """获取哈希表中字段的值"""
        return self.client.hget(key, field)

    def get_all_hash(self, key: str) -> Optional[dict]:
        """获取哈希表中的所有字段和对应值"""
        return self.client.hgetall(key)

    # 列表类型操作
    def push_to_list(self, key: str, value: Any, expire_time: Optional[int] = None) -> int:
        """将元素推送到列表的左端，并可指定过期时间"""
        result = self.client.lpush(key, value)
        if expire_time:
            self.client.expire(key, expire_time)
        return result

    def pop_from_list(self, key: str) -> Optional[str]:
        """从列表的左端弹出元素"""
        return self.client.lpop(key)

    def get_list(self, key: str, start: int = 0, end: int = -1) -> List[str]:
        """获取列表中的指定区间的元素"""
        return self.client.lrange(key, start, end)

    # 集合类型操作
    def add_to_set(self, key: str, value: Any, expire_time: Optional[int] = None) -> int:
        """将元素添加到集合，并可指定过期时间"""
        result = self.client.sadd(key, value)
        if expire_time:
            self.client.expire(key, expire_time)
        return result

    def remove_from_set(self, key: str, value: Any) -> int:
        """从集合中移除元素"""
        return self.client.srem(key, value)

    def get_set(self, key: str) -> set:
        """获取集合中的所有元素"""
        return self.client.smembers(key)

    # 有序集合操作
    def add_to_sorted_set(self, key: str, score: float, value: Any, expire_time: Optional[int] = None) -> int:
        """将元素添加到有序集合，并可指定过期时间"""
        result = self.client.zadd(key, {value: score})
        if expire_time:
            self.client.expire(key, expire_time)
        return result

    def get_sorted_set(self, key: str, start: int = 0, end: int = -1) -> List[Union[str, float]]:
        """获取有序集合中的指定区间元素"""
        return self.client.zrange(key, start, end, withscores=True)

    # 删除操作
    def delete(self, key: str) -> bool:
        """删除指定的键"""
        return self.client.delete(key)

    # 检查键是否存在
    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        return self.client.exists(key)

    # 清空数据库
    def flush_db(self) -> bool:
        """清空当前数据库"""
        return self.client.flushdb()

    # 获取数据库中的所有键
    def get_all_keys(self) -> List[str]:
        """获取所有键"""
        return self.client.keys('*')

    # 设置键的过期时间（单位：秒）
    def set_expire(self, key: str, expire_time: int) -> bool:
        """设置指定键的过期时间（单位：秒）"""
        return self.client.expire(key, expire_time)

    # 获取剩余的过期时间（单位：秒）
    def ttl(self, key: str) -> int:
        """获取键的剩余过期时间（单位：秒）"""
        return self.client.ttl(key)

# 示例使用
if __name__ == "__main__":
    redis_client = RedisClient(password='002161')  # 提供密码

    # 设置字符串并指定过期时间（10秒）
    redis_client.set_string('temp_key', 'temporary_value', expire_time=10)
    print(redis_client.get_string('temp_key'))  # 输出 temporary_value
    time.sleep(12)  # 等待超过过期时间
    print(redis_client.get_string('temp_key'))  # 输出 None，表示键已过期

    # 设置哈希并指定过期时间（5秒）
    redis_client.set_hash('my_hash', 'field1', 'value1', expire_time=5)
    print(redis_client.get_hash('my_hash', 'field1'))  # 输出 value1
    time.sleep(6)  # 等待超过过期时间
    print(redis_client.get_hash('my_hash', 'field1'))  # 输出 None，表示键已过期

    # 设置列表并指定过期时间（15秒）
    redis_client.push_to_list('my_list', 'item1', expire_time=15)
    print(redis_client.get_list('my_list'))  # 输出 ['item1']
    time.sleep(16)  # 等待超过过期时间
    print(redis_client.get_list('my_list'))  # 输出 [], 表示键已过期