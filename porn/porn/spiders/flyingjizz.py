import scrapy
from ..items import PornItem
from scrapy.http import Request
import js2xml
import lxml.etree
from parsel import Selector
import xml.etree.ElementTree as ET

class FlyingjizzSpider(scrapy.Spider):
    name = 'flyingjizz'
    start_urls = ['https://www.flyingjizz.com/videos/site/babes/']

    def parse(self, response):
        thumbnail_urls = response.css('.thumbnail > a ::attr(src)').getall()
        video_urls = response.css('.thumbnail > a ::attr(href)').getall()
        titles = response.css('.caption a ::text').getall()

        clean_video_urls = []
        for video_url in video_urls:
            clean_video_urls.append(response.urljoin(video_url))

        for i in range(len(thumbnail_urls)):

            item = PornItem()

            item['title'] = titles[i]
            item['thumbnail_link'] = thumbnail_urls[i]
            item['video_link'] = clean_video_urls[i]

            yield Request(url=clean_video_urls[i], callback=self.video_page, meta={'item': item})

        next_page = response.css('.next a ::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)

    def video_page(self,response):
        javascript = response.css('script::text').get()
        xml = lxml.etree.tostring(js2xml.parse(javascript), encoding='unicode')
        selector = Selector(text=xml)
        video_selector = selector.css('var[name="flashvars"]').get()
        video_link = ET.fromstring(video_selector)
        v = 'https://flyingjizz.com' + video_link[0][3][0].text

        item = response.meta.get('item')
        item['video_location'] = v
        yield item
