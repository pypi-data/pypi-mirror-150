# # -*- coding: utf-8 -*-
# """
# msab.common.redisMgr.py
# v1.0
# ~~~~~~~~~~~~~~~~~~~~~~~

# :copyright: (c) 2018-2022 by the Ji Fu, see AUTHORS for more details.
# :license: MIT, see LICENSE for more details.
# """

# from msab.exts import r_client
# from ..SingletonExt import Singleton


# @Singleton
# class RedisMgr():
#     """
#     >>> Redis Manager
#     """

#     @classmethod
#     def set_value(cls, key, value, expire_time=864000):
#         """
#         >>> 设置key value
#         :param {String} key: 键名称
#         :param {String} value: 键值
#         :param {Int} expire_time: 过期时间 (default 60s * 60m * 24h * 10 d)
#         :returns {}:
#         """
#         if isinstance(key, str):
#             r_client.set(key, value)
#             r_client.expire(key, expire_time)
#             return r_client.get(key)
#         return None

#     @classmethod
#     def get_value(cls, key):
#         """
#         >>> 获取key value
#         :param {String} key: 键名称
#         :returns {String}: 键值
#         """
#         return r_client.get(key)

#     @classmethod
#     def get_value_by_prefix(cls, key_prefix):
#         """
#         >>> 通配符获取 Key Value
#         :param {String} key_prefix: 键名 通配符
#         :returns {List<String>}: list<键名key>
#         """
#         return r_client.keys(pattern="{}.*".format(key_prefix))

#     @classmethod
#     def insert_set(cls, key, value, expire_time=8640000):
#         """
#         >>> 插入 set 值
#         :param {String} key: set键名称
#         :param {String} value: 键值
#         :param {Int} expire_time: 过期时间 (default 60s * 60m * 24h * 10 d)
#         :returns {Boolean}: 插入结果
#         """
#         if isinstance(key, str):
#             r_client.sadd(key, value)
#             r_client.expire(key, expire_time)
#             return True
#         return None

#     @classmethod
#     def get_set(cls, key):
#         """
#         >>> 获取 set 内容
#         :param {String} key: set键名称
#         :param {String} value: 键值
#         :returns {List<String>}: set 值
#         """
#         return r_client.smembers(key)

#     @classmethod
#     def insert_list(cls, key, value, expire_time=864000):
#         """
#         >>> 插入队列
#         :param {String} key: 键名称
#         :param {String} value: 键值
#         :param {Int} expire_time: 过期时间 (default 60s * 60m * 24h * 10 d)
#         :returns {list<>}: 插入后队列内容
#         """
#         if isinstance(key, str):
#             r_client.lpush(key, value)
#             r_client.expire(key, expire_time)
#             return cls.get_list(key)
#         return None

#     @classmethod
#     def pop_list(cls, key):
#         """
#         >>> 出队
#         :param {String} key: set键名称
#         :returns {List<String>}: set
#         """
#         return r_client.lpop(key)

#     @classmethod
#     def get_list(cls, key):
#         """
#         >>> 获取队列内容
#         :param {String} key: set键名称
#         :returns {List<String>}: set
#         """
#         llen = r_client.llen(key)
#         return r_client.lrange(key, 0, llen)

#     @classmethod
#     def remaining(cls, key):
#         """
#         >>> 查询过期时间
#         :param {String} key: 键名称
#         :param {Int}: 过期时间
#         """
#         return r_client.ttl(key)

#     @classmethod
#     def rm_key(cls, key):
#         """
#         >>> 删除键
#         :param {String} key: 键名称
#         :returns {Boolean}: 插入结果
#         """
#         return r_client.delete(key)

#     @classmethod
#     def rm_keys(cls, key_prefix):
#         """
#         >>> 删除一组键值对
#         :param {String} key_prefix: 键名称 prefix
#         :returns {Boolean}: 插入结果
#         """
#         keys = r_client.keys("{}*".format(key_prefix))
#         for key in keys:
#             r_client.delete(key)

#     @classmethod
#     def reflush_db(cls):
#         """
#         >>> 清空应用 cache
#         """
#         cache_keys = r_client.keys("msab.cache*")
#         for i in cache_keys:
#             r_client.delete(i)
