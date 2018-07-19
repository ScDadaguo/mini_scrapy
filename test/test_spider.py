from gevent import monkey
monkey.patch_all()
from spider import Spider
from http_client.request import Request

class TestSpider(Spider):

    """ TestSpider """

    start_urls = [
        "http://news.baidu.com/",
        "https://tieba.baidu.com/index.html",
        "https://zhidao.baidu.com/",
        "http://music.taihe.com/",
        "http://v.baidu.com/",
        "http://image.baidu.com/",
        "https://map.baidu.com/"
    ]

    def parse(self, response):

        print(response.url,len(response.body))
        # yield {"url": response.url, "status": response.status}
        # yield Request("http://movie.douban.com/review/best/",
        #               callback=self.parse_best)

        yield  Request("http://v.baidu.com/tv/27812.htm?frp=browse",callback=self.parse_best)

    def parse_best(self, response):
        print(len(response.body))


def main():
    spider = TestSpider()
    spider.start()


if __name__ == "__main__":
    main()