import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class GansuNewsSpider(Spider):
    def __init__(self):
        super(GansuNewsSpider, self).__init__()
    
    name = "gansunews"
    original_url = "http://www.gansu.gov.cn"

    def start_requests(self):
        url = "http://www.gansu.gov.cn/col/col10345/index.html"
        yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)

    def parse(self,response):
        sel = Selector(response)
        detail_page_info = sel.xpath('//div[@class="default_pgContainer"]//li')
        for info in detail_page_info:
            detail_page_url = info.xpath('./a/@hret').extract_first()
            detail_url = self.original_url + detail_page_url
            print(detail_url)
            yield scrapy.Request(url=detail_url,meta={"detail_url":detail_url},callback=self.detail_parse,dont_filter=True)

    def detail_parse(self,response):
        item = BaseDataItem()
        sel = Selector(response)
        item["detail_url"] = response.meta["detail_url"]
        item["location"] = "甘肃"
        item["publish_time"] = ""  #时间在正文里的更准确
        title = sel.xpath('//table[@width="95%"]//td/text()').extract_first()
        item["title"] = title
        content = ""
        content_text = sel.xpath('//td[@class="bt_content"]//p//text()').extract()
        for row in content_text:
            content = content + row.strip() + "\n"
        item["content"] = content

        attend_persons = ""
        attend_persons_text = sel.xpath('//td[@class="bt_content"]//p//span/text()').extract()
        for per in attend_persons_text:
            attend_persons = attend_persons + per.strip() + "\n"
        item["attend_persons"] = attend_persons
        
        summary = ""
        summary_text = sel.xpath('//meta[@name="description"]/content/text()').extract()
        for sum in summary_text:
            summary = summary + sum.strip() + "\n"
        item["summary"] = summary
        print(item)
        # yield item
        