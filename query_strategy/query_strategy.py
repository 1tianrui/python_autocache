# coding=utf-8
from repository.repository import StrategyMethodNotImplException


class QueryStrategy(object):
    # 获取查询条件
    def query_params(self):
        raise StrategyMethodNotImplException

    # 根据查询条件生成db查询的dict
    def db_query_param(self):
        raise StrategyMethodNotImplException

    # 将查询结果按照查询条件顺序进行排序
    def sort(self, cache_content, cache_strategy):
        raise StrategyMethodNotImplException

    # 封装缓存失效的条件  缓存不存在 or 缓存内容失效 , 并生成新的查询策略
    def generate_cache_miss_query(self, cache_content, cache_strategy):
        raise StrategyMethodNotImplException
