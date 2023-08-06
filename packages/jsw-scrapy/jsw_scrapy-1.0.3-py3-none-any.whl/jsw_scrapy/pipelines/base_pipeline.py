from itemadapter import ItemAdapter


class BasePipeline:
    ENTITY_MAPPING = {}
    ENTITY_AUTO_SAVE = False

    def __init__(self):
        self.adapter = None

    @property
    def item_dict(self):
        return self.adapter.asdict()

    def process_item(self, item, spider):
        method_name = "process_" + spider.name
        self.adapter = ItemAdapter(item)
        if self.ENTITY_AUTO_SAVE:
            self.save_entity(item, spider)
        if hasattr(self, method_name):
            return getattr(self, method_name)(item, spider)
        return item

    def get_id(self, item, spider):
        return {'id': item['id']}

    def save_entity(self, item, spider):
        spider.logger.debug('Processing entity: %s', self.item_dict)
        id_dict = self.get_id(item, spider)
        entity = self.ENTITY_MAPPING[spider.name].first_or_create(**id_dict)
        entity.update(**item) if item else None
        entity.save()
        return item

    def fill_entity(self, **kwargs):
        entity_class = kwargs.get('entity_class')
        item = kwargs.get('item')
        entity = entity_class()
        entity.fill(**item)
        entity.save()
