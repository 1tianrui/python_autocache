# coding=utf-8
from cache_util import CacheUtil

"""
*CacheStrategy*
封装缓存相关决策(缓存key生成 ,缓存数据结构转换)
*QueryStrategy*
封装查询参数，提供db查询参数的自定义 ,并提供根据查询参数排序
*Repository*
持有数据库和缓存的访问句柄，调用 cacheStrategy 和 queryStrategy 完成查询主流程
*IdQueryStrategy*
基于单个键的查询实现 
eg:
def multi_get(ids)
     repo = SaleItemRepository(Model, MemcachedClient)
     query_strategy = IdQueryStrategy('source_id',item_ids)
     cache_strategy = UDF_CACHE_STRATEGY()
     return cls.repo.multi_get(cache_strategy,query_strategy)
"""


class StrategyMethodNotImplException(Exception):
    def __init__(self, err='method not implement'):
        Exception.__init__(self, err)


class Repository(object):
    def __init__(self, model, cache_client, supported_cache_strategy_classes=None):
        self.model = model
        self.cache_client = cache_client
        self.cache_strategy_classes = supported_cache_strategy_classes

    def get(self, cache_strategy, query_strategy):
        cache_content = CacheUtil.get(query_strategy, cache_strategy, self.cache_client)
        if not cache_content:
            db_query_param = query_strategy.db_query_param()
            db_content = self.model.objects(**db_query_param).first()
            if db_content:
                cache_content = CacheUtil.set(db_content, query_strategy, cache_strategy, self.cache_client)
        return cache_content

    def multi_get(self, cache_strategy, query_strategy):
        cache_content = CacheUtil.multi_get(query_strategy, cache_strategy, self.cache_client)
        sub_query_strategy = query_strategy.generate_cache_miss_query(cache_content, cache_strategy)
        db_params = sub_query_strategy.db_query_param()
        db_contents = self.model.objects(**db_params)
        if db_contents:
            tmp_cache = CacheUtil.multi_set(db_contents, cache_strategy, self.cache_client)
            cache_content.update(tmp_cache)
        return CacheUtil.sort(cache_content, query_strategy, cache_strategy)

    def objects(self, params):
        return self.model.objects(params)

    def update(self, db_content, update_params):
        db_content.update(**update_params)

    def __post_update(self, db_content):
        if not self.cache_strategy_classes:
            return
        for cache_strategy_class in self.cache_strategy_classes:
            cache_strategy = cache_strategy_class()
            key = cache_strategy.dump_k(db_content)
            value = cache_strategy.dump_v(db_content)
            self.cache_client.set(key, value)
