
import scrapy

class PornItem(scrapy.Item):
    title = scrapy.Field()
    thumbnail_link = scrapy.Field()
    video_link = scrapy.Field()
    video_location = scrapy.Field()
    
