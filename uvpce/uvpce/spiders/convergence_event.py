import scrapy
from scrapy.http import FormRequest

class AlluminaiSpider(scrapy.Spider):
    name = 'convergence_event'
    start_urls = ['https://convergence.uvpce.ac.in/login']

    def parse(self, response):
        return FormRequest.from_response(response,
            formdata = {"email":"aasshish13@gmail.com","password":"9687655755"},
            method = 'post',
            callback = self.start_scrapy)

    def start_scrapy(self,response):
        events = response.css("#headingTwo a::text").getall()
        for i in range(len(events)):
            yield {
                'event_name': events[i].strip()
            }

# response.url.split('/')[-1]

