# coding=utf-8


class CacheUtil(object):
    # 统一处理id 到 缓存key的映射问题
    @classmethod
    def multi_get(cls, query_strategy, cache_strategy, cache_client):
        keys = cache_strategy.keys(query_strategy.query_params())
        cache_result = cache_client.get_multi(keys)
        return cache_result

    @classmethod
    def multi_set(cls, db_contents, cache_strategy, cache_client):
        cache_result = {}
        for db_content in db_contents:
            k, v = cache_strategy.dump_kv(db_content)
            cache_result[k] = v
        cache_client.save_multi(cache_result)
        return cache_result

    @classmethod
    def multi_remove(cls, ids, scheme, cache_client):
        keys = scheme.keys(ids)
        contents = [None] * len(ids)
        cache_map = dict[zip(keys, contents)]
        cache_client.save_multi(cache_map)

    @classmethod
    def get(cls, query_strategy, cache_strategy, cache_client):
        key = cache_strategy.key(query_strategy.query_params())
        return cache_client.get(key)

    @classmethod
    def set(cls, db_content, query_strategy, cache_strategy, cache_client):
        key = cache_strategy.key(query_strategy.query_params())
        cache_content = cache_strategy.dump(db_content)
        cache_client.save(key, cache_content)
        return cache_content

    @classmethod
    def sort(cls, cache_content, query_strategy, cache_strategy):
        return query_strategy.sort(cache_content, cache_strategy)
