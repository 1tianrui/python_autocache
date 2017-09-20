# coding=utf-8
from repository.repository import StrategyMethodNotImplException


class CacheStrategy(object):
    # 生成缓存key
    def key(self, query_params):
        raise StrategyMethodNotImplException

    # 生成缓存key的list
    def keys(self, query_params):
        raise StrategyMethodNotImplException

    # 将orm对象装成 缓存存储对象
    def dump(self, db_content):
        raise StrategyMethodNotImplException

    # orm对象转成 k,v对象
    def dump_kv(self, db_content):
        raise StrategyMethodNotImplException
