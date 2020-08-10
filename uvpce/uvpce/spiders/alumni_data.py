import scrapy
from scrapy.http import FormRequest, Request, TextResponse
import json
import ast
from dotenv import load_dotenv
load_dotenv()

class AlluminaiSpider(scrapy.Spider):
    name = 'alumni_data'
    start_urls = ['https://alumni.ganpatuniversity.ac.in/api/login/loginUser']

    count = 1
    cookies_dict = {}

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
   
        for i in cookies:
            cookies_pretty = i.split(';')[0].split('=')
            self.cookies_dict[cookies_pretty[0]] = cookies_pretty[1]

        return Request(
            url = "https://alumni.ganpatuniversity.ac.in/api/search/filterCount",
            method = "post",
            body=json.dumps({"other_params":{"fetch_lost":True,"roles":[1,2],"rollup_by":["subinst","yop","degree","department"],"actual_rollup":True,"no_streaming":True},"queryString":{},"subinst":["14"]}),
            cookies = self.cookies_dict,
            callback = self.process_of_fetching
            )
    
    def process_of_fetching(self,response):

        res = json.loads(response.body.decode('utf-8'))
        for i in res["data"]:
            if i["degree"] != None and i["department"] != None:
                
                yield Request(
                        url = "https://alumni.ganpatuniversity.ac.in/api/search/UserSearch",
                        method = "post",
                        body=json.dumps({"subinst":[int(i["subinst"])],"yoj":[],"yop":[int(i["yop"])],"degree":[int(i["degree"])],"department":[int(i["department"])],"stream":self.count,"lm":10,"other_params":{"fetch_lost":True,"roles":[1,2]},"queryString":{}}),
                        cookies = self.cookies_dict,
                        callback = self.start_scrapy
                        )

    def start_scrapy(self,response):

        data = json.loads(response.body.decode('utf-8'))

        if data["success"] == 1:

            for i in data["data"]:
                yield {
                    'Name': i["basic_info"]["name"].upper(),
                    'Department': i["basic_info"]["department"].upper(),
                    'City': i["basic_info"]["city"],
                    'Start_year': i["basic_info"]["start"],
                    'End_year': i["basic_info"]["end"],
                    'Image': "https://almashines.s3.dualstack.ap-southeast-1.amazonaws.com/"+i["basic_info"]["profile_pic"]["large"] if i["basic_info"]["profile_pic"]["large"] != None else None,
                }

            # print(json.loads(response.request.body.decode('utf-8'))["subinst"])
            req_details = json.loads(response.request.body.decode('utf-8'))
            yield Request(
                url = "https://alumni.ganpatuniversity.ac.in/api/search/UserSearch",
                method = "post",
                body=json.dumps({"subinst": req_details["subinst"],"yoj":[],"yop":req_details["yop"],"degree":req_details["degree"],"department":req_details["department"],"stream":req_details["stream"] + 1,"lm":10,"other_params":{"fetch_lost":True,"roles":[1,2]},"queryString":{}}),
                cookies = self.cookies_dict,
                callback = self.start_scrapy
                )


