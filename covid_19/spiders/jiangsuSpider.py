import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from urllib.parse import urlencode
from covid_19.items import BaseDataItem

class JiangsuSpider(Spider):
    name="jiangsu"
    def __init__(self):
        self.since = 0
        self.data_param = {
            'webid':"1",
            'columnid':"60096",
            'unitid':"212860"
        }
        super(JiangsuSpider, self).__init__()
    
    def start_requests(self):
        
        post_url = "http://www.jiangsu.gov.cn/module/web/jpage/dataproxy.jsp?startrecord=1&endrecord=40&perpage=40"
        yield scrapy.FormRequest(url=post_url,method="POST",formdata=self.data_param ,headers={"Content_type":"application/x-www-form-urlencoded"},callback=self.parse,dont_filter=True)

    def parse(self,response):
        sel = Selector(response)
        records = sel.xpath("//record").extract()
        for record in records[:-1]:
            detail_url = re.findall(r'<.*?a.*?href="(.*?)" title', record, re.I|re.S|re.M)[0]
            title =re.findall(r'<.*?a.*?title="(.*?)" target', record, re.I|re.S|re.M)[0]
            # 可以看一下能否处理一下publish_time的正则，从这里获取
            publish_time = re.findall('.*?<span>(.*?)</span>',record,re.M)[0]
            yield scrapy.Request(url=detail_url,meta={"detail_url":detail_url,"title":title,"publish_time":publish_time},callback=self.detail_parse,dont_filter=True)

        if len(records)==41:
            self.since += 40
            url = "http://www.jiangsu.gov.cn/module/web/jpage/dataproxy.jsp?startrecord=%s&endrecord=%s&perpage=40"%(str(self.since),str(self.since+40))
            yield scrapy.FormRequest(url=url,method="POST",formdata=self.data_param ,headers={"Content_type":"application/x-www-form-urlencoded"},callback=self.parse,dont_filter=True)

    def detail_parse(self,response):
        detail_url = response["detail_url"]
        title = response["title"]
        publish_time = response["publish_time"]
        sel = Selector(response)
        content = sel.xpath('//div[@id="zoom"]/p/text()').extract_first()
        item = BaseDataItem()
        item["detail_url"] = detail_url
        item["title"] = title
        item["publish_time"] = publish_time
        item["location"] = "江苏"
        item["attend_persons"]=""
        item["summary"]=""
        item["content"]=content
        yield item

        
        