import datetime
import urllib.parse
from abc import abstractmethod, ABC

import requests
from bs4 import BeautifulSoup
from dateutil import parser


class NewsBase(ABC):
    def __init__(self, base_url: str, api: str):
        self.base_url = base_url
        self.api = api
        self.news_dict = {}

    def make_soup(self, params: dict) -> BeautifulSoup:
        url = urllib.parse.urljoin(self.base_url, self.api)
        res = requests.get(url, params).text
        soup = BeautifulSoup(res, features='lxml')
        return soup

    @abstractmethod
    def get_all_news(self, soup: BeautifulSoup) -> BeautifulSoup:
        pass

    @abstractmethod
    def get_news_date(self, news: BeautifulSoup) -> datetime:
        pass

    @abstractmethod
    def get_news_url(self, news: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def get_news_title(self, news: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def update_all_qualify_news(self, keyword: str, condition: str):
        pass

    def whether_today_news(self, news: BeautifulSoup) -> bool:
        news_date = self.get_news_date(news)
        if news_date.date() == datetime.datetime.today().date():
            return True
        else:
            return False


class ChainNews(NewsBase):
    def get_all_news(self, soup: BeautifulSoup) -> list:
        news = soup.find_all(class_="feed-item feed-item-news")
        return news

    def get_news_date(self, news: BeautifulSoup) -> datetime.date:
        # 输入单条news的soup返回该news的发布日期
        return parser.parse(news.find(class_="post-time").get('datetime'))

    def get_news_url(self, news: BeautifulSoup) -> str:
        # 输入单条news的soup返回该news的url
        return urllib.parse.urljoin(self.base_url, news.find('a').get('href'))

    def get_news_title(self, news: BeautifulSoup) -> str:
        # 输入单条news的soup返回该news的title
        return news.find('a').get('title')

    def update_all_qualify_news(self, params: dict, condition: str): #TODO 使用协程去做数据获取
        news_soup = self.make_soup(params)
        news_list = self.get_all_news(news_soup)
        if condition == 'today':
            for news in news_list:
                news_title = self.get_news_title(news)
                news_url = self.get_news_url(news)
                if self.whether_today_news(news):
                    self.news_dict.update({news_title: news_url})
        elif condition == "all":
            for news in news_list:
                news_title = self.get_news_title(news)
                news_url = self.get_news_url(news)
                self.news_dict.update({news_title: news_url})

if __name__ == '__main__':
    cn = ChainNews("https://www.chainnews.com/", "search?")
    cn.update_all_qualify_news( {"q": "btc"},"all")
    cn.update_all_qualify_news({"q":"eth"},"all")
    print(cn.news_dict)
