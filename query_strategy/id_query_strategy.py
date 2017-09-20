# coding=utf-8
from repository.strategy.query_strategy.query_strategy import QueryStrategy


class IdQueryStrategy(QueryStrategy):
    def __init__(self, id_name, id_query_param):
        self.id_query_param = id_query_param
        self.id_name = id_name

    # 返回无缓存或者缓存失效的 查询条件
    def generate_cache_miss_query(self, cache_content, cache_strategy):
        no_cache_params = []
        for query_param in self.id_query_param:
            key = cache_strategy.key(query_param)
            if not cache_content.get(key):
                no_cache_params.append(query_param)
        return IdQueryStrategy(self.id_name, no_cache_params)

    def db_query_param(self):
        if isinstance(self.id_query_param, list):
            query_dict = {}
            query_dict[self.id_name + "__in"] = self.id_query_param
        else:
            query_dict = {}
            query_dict[self.id_name] = self.id_query_param
        return query_dict

    def query_params(self):
        return self.id_query_param

    def sort(self, cache_contents, cache_strategy):
        ids = self.id_query_param
        result = []
        for id in ids:
            key = cache_strategy.key(id)
            cache_content = cache_contents.get(key)
            if cache_content:
                result.append(cache_content)
        return result
