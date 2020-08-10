import scrapy
import re

class UvpceSpider(scrapy.Spider):
    name = 'uvpce'
    allowed_domains = ['www.uvpce.ac.in']
    start_urls = [
        'https://www.uvpce.ac.in/ce-faculty',
        'https://www.uvpce.ac.in/it-faculty',
        'https://www.uvpce.ac.in/me-faculty',
        'https://www.uvpce.ac.in/marine-faculty',
        'https://www.uvpce.ac.in/bm-faculty',
        'https://www.uvpce.ac.in/mc-faculty',
        'https://www.uvpce.ac.in/ec-faculty',
        'https://www.uvpce.ac.in/cv-faculty',
        'https://www.uvpce.ac.in/ele-faculty',
    ]

    def parse(self, response):
        branch = response.url.split('/')[-1].split('-')[0]
        Faculties = response.css("#block-system-main a::text").getall();
        Experience = response.css(".views-field-field-experience .field-content::text").getall();
        Email = response.css(".views-field-field-email-address .field-content::text").getall();
        Designation = response.css(".views-field-field-present-designation .field-content::text").getall();
        Image = response.css("#block-system-main img::attr(src)").getall();

        for i in range(len(Faculties)):
            yield {
                'Faculty_name': Faculties[i],
                'Experience': Experience[i],
                'Email': self.email_validator(Email[i]),
                'Designation': Designation[i],
                'Image': Image[i],
                'Branch': branch
            }
    
    def email_validator(self,email):
        email = re.sub(re.escape('[at]'), '@', email, flags=re.IGNORECASE)
        email = re.sub(re.escape('[dot]'), '.', email, flags=re.IGNORECASE)
        email = re.sub(re.escape('[in]'), '.in', email, flags=re.IGNORECASE)
        return email

        
