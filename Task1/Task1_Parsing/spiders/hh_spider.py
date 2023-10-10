import scrapy


class hh_spider(scrapy.Spider):
    name = "hh_spider"
    allowed_domains = ["nn.hh.ru"]
    start_urls = ["https://nn.hh.ru/vacancies/data-analyst",
                  "https://nn.hh.ru/vacancies/data-scientist"]

    
    def parse(self, response, **kwargs):
        header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.967 YaBrowser/23.9.1.967 Yowser/2.5 Safari/537.36",
        }
    
        for h3 in response.xpath('//h3/span/a'):
            href = h3.xpath('@href').get()
            index_to_delete_after = href.find('?')
            url = href[:index_to_delete_after]
            
            yield scrapy.Request(url, headers=header, callback=self.parse_vacancy)
            
            
    def parse_vacancy(self, response, **kwargs):
        item = {'vacancy_name': response.xpath('//h1/text()').get(),
                'work_experience': response.xpath('//p/span/text()').get()
                }
       
        yield item 
            
    