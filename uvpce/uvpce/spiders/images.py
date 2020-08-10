import scrapy


class ImagesSpider(scrapy.Spider):
    name = 'images'
    start_urls = ['https://thegatewaycorp.com/spotlight/']

    def parse(self, response):
        print(response.status)
        image_urls = response.css('img ::attr(src)').getall()
        print(image_urls)

        for i in image_urls:
            yield {
                "image_urls": image_urls
            }
        

