import scrapy
import jsw_nx as nx
from fake_useragent import UserAgent


class BaseSpider(scrapy.Spider):
    handle_httpstatus_list = [400]
    url = None
    ua = UserAgent()
    ua_pc = 'Mozilla/5.0 zgrab/0.x'
    ua_mobile = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) By aric.zheng/0.x'
    ua_random = ua.chrome

    def get_un_crawled(self, **kwargs):
        # required:
        entity_class = kwargs.get('entity_class')
        # optional:
        crawled = kwargs.get('crawled', {'is_crawled': False})
        options = crawled.merge(kwargs.get('options', {}))
        limit = kwargs.get('limit', None)

        if limit:
            return entity_class.where(options).take(limit).get()
        else:
            return entity_class.where(options).get()

    def update_crawled(self, **kwargs):
        record = kwargs.get('record')
        crawled = kwargs.get('crawled', 'is_crawled')
        setattr(record, crawled, True)
        record.save()

    def noop_request(self):
        yield scrapy.Request(url="https://www.baidu.com", callback=nx.noop_scrapy_parse)
