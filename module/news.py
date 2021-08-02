import datetime
import urllib.parse
from abc import abstractmethod, ABC

import pandas as pd
import requests
from bs4 import BeautifulSoup
from dateutil import parser


class NewsParser:
    def __init__(self):
        self.news_dataframe = pd.DataFrame(columns=["news_title", "news_url"])

    def update_news(self, **kwargs):
        self.news_dataframe = self.news_dataframe.append(pd.Series(kwargs), ignore_index=True)


class NewsAdapter: #FIXME
    # adapt every news class:
    def __init__(self):
        pass



class NewsBase(ABC):
    def __init__(self, news_parser: NewsParser = None):
        if news_parser is None:
            self.news_parser = NewsParser()
        else:
            self.news_parser = news_parser

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

    def whether_yesterday_news(self, news: BeautifulSoup) -> bool:
        news_date = self.get_news_date(news)
        if news_date.date() == datetime.datetime.yesterday().date():
            return True
        else:
            return False


class ChainNews(NewsBase):
    def __init__(self, news_parser):
        super().__init__(news_parser)
        self.base_url = "https://www.chainnews.com/"
        self.api = "search?"

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

    def update_all_qualify_news(self, params: dict, condition: str):  # TODO 使用协程去做数据获取
        news_soup = self.make_soup(params)
        news_list = self.get_all_news(news_soup)
        for news in news_list:
            news_title = self.get_news_title(news)
            news_url = self.get_news_url(news)
            if condition.lower() == 'today':  # TODO python3.10以后改成switch ...  case ...
                if self.whether_today_news(news):
                    self.news_parser.update_news(news_title=news_title, news_url=news_url)
            elif condition.lower() == "yesterday":
                if self.whether_yesterday_news(news):
                    self.news_parser.update_news(news_title=news_title, news_url=news_url)
            elif condition.lower() == "all":
                self.news_parser.update_news(news_title=news_title, news_url=news_url)
            else:
                raise ValueError("input wrong condition")


if __name__ == '__main__':
    cn = ChainNews(NewsParser())
    cn.update_all_qualify_news({"q": "btc"}, "all")
    cn.update_all_qualify_news({"q": "eth"}, "all")
    print(cn.news_parser.news_dataframe)
