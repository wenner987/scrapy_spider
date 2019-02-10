from scrapy.spiders import Spider
from bs4 import BeautifulSoup
import scrapy
import os

class Sp1(Spider):
    root_url = """https://www.fpzw.com/xiaoshuo/81/81501/"""
    start_urls = [ """https://www.fpzw.com/xiaoshuo/81/81501/"""]
    name = """spider1"""
    bufen = 0

    def parse (self, response):
        res = response.xpath("/html/body/dl/dd")
        for i in res:
            print (i.xpath("./text()").extract()[0])
            obj = i.xpath ("./a/@href").extract()
            try:
                urls = obj[0]
            except:
                print("continue!")
            try:
                if urls== "" or (i.xpath("/text()").extract()[0])[0:1] != "第":
                    continue
            except:
                print("continue!")
            yield scrapy.Request(
                url=self.root_url+urls,
                callback=self.parse_get,
                meta=response.meta
            )
            exit

    def parse_get (self, response):
        select = response.xpath ("""//p[@class="Text"]/text()""").extract();
        tittle = response.xpath("""//h2/text()""").extract()[0]
        print ("第"+str(self.bufen)+"部分"+tittle)  # log
        if tittle[1:4] == "第一章":
            self.bufen = self.bufen + 1
        if os.path.exists("/home/wenner/workspace/programe/xiaoshuo/"+ str(self.bufen)) == False:
            os.mkdir("/home/wenner/workspace/programe/xiaoshuo/"+ str(self.bufen))
        with open ("/home/wenner/workspace/programe/xiaoshuo/"+ str(self.bufen) + "/" + tittle, "wb+") as f:
            for strs in select:
                f.write (strs.encode(response.encoding) + b"\n")