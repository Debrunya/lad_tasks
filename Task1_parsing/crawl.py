import os
from scrapy import cmdline


def crawl():
    os.chdir("spiders")
    cmdline.execute("scrapy runspider hh_spider.py -o ../vacancies.json".split())
    os.chdir("..")


if __name__ == '__main__':
    
    #спарсим сайт hh.ru с помощью паука scrapy
    crawl()