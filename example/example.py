from cache_strategy.cache_strategy import CacheStrategy
import json
from repository import  Repository
from query_strategy.id_query_strategy import  IdQueryStrategy
class YourCacheStrategy(CacheStrategy):
    def __init__(self, key_pre):
        self.key_pre = key_pre

    def key(self, id):
        return self.key_pre % id

    def keys(self, ids):
        return [self.key_pre % id for id in ids]

    def dump_k(self, db_content):
        return self.key_pre % db_content.id

    def dump_v(self, db_content):
        return json.dumps(db_content)


class Test :
    repo = Repository(YourDocument, YourCacheClient)

    @classmethod
    def multi_get_item_detail(cls, item_ids):
        query_strategy = IdQueryStrategy('id', item_ids)
        cache_strategy = YourCacheStrategy()
        return cls.repo.multi_get(cache_strategy, query_strategy)
