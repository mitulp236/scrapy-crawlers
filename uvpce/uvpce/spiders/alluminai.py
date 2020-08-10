import scrapy
from scrapy.http import FormRequest, Request, TextResponse
import json
import os
from dotenv import load_dotenv
load_dotenv()


class AlluminaiSpider(scrapy.Spider):
    name = 'alluminai'
    start_urls = ['https://alumni.ganpatuniversity.ac.in/api/login/loginUser']

    counnt = 1
    def parse(self, response):
        return Request(
            url="https://alumni.ganpatuniversity.ac.in/api/login/loginUser",
            method="post",
            body=json.dumps({"email":os.getenv("ganpat_uni_alumni_email"),"password":os.getenv("ganpat_uni_alumni_password"),"force_signup_cid":"11"}),
            callback=self.after_login
            )

    def after_login(self,response):

        cookies = []
        for i in response.headers.getlist("Set-Cookie"):
            cookies.append(i.decode('utf-8'))

        cookies_dict = {}
        for i in cookies:
            cookies_pretty = i.split(';')[0].split('=')
            cookies_dict[cookies_pretty[0]] = cookies_pretty[1]

        return Request(
            url = "https://alumni.ganpatuniversity.ac.in/api/jobs/fetch_community_jobs",
            method = "post",
            body=json.dumps({"stream":self.counnt}),
            cookies = cookies_dict,
            callback = self.start_scrapy
            )

    # def next_page(self, response):
    #     return 

    def start_scrapy(self,response):

        data = json.loads(response.body.decode('utf-8'))

        if data["success"] == 1:

            for i in data["data"]:
                yield {
                    'Company_name': i["company"],
                    'Designation': i["designation"],
                    'City': i["city"],
                    'salary': i["salary"],
                    'job_type': "job" if i["job_type"] == "0" else "internship",
                    'duration': i["duration"],
                    'Description': i["company_desc"],
                }
            print(self.counnt)
            self.counnt = self.counnt + 1
            yield Request(url="https://alumni.ganpatuniversity.ac.in/api/jobs/fetch_community_jobs",callback=self.after_login,dont_filter=True)
        



