import asyncio
import logging

from news import *


class Collection:
    # 通过协程的方式收集信息
    def __init__(self):
        self.news_parser = NewsParser()

    def collect_all_news(self, news_params_list: list):
        asyncio.run(self._collect_all_news(news_params_list))

    async def _collect_news(self, news: NewsBase, params: dict, condition: str):
        logging.info("Start collect news")
        news(self.news_parser).update_all_qualify_news(params, condition)
        await asyncio.sleep(0.5)
        logging.info("Finish collect")

    async def _collect_all_news(self, news_params_list: list):
        """
        用携程的方式对news及参数做遍历获取处理
        param: news_params_list = [{"news":xxx,"params":xxx,"condition":xxx}] :
        """
        name = locals()
        for i, news_params in enumerate(news_params_list):
            name[f"task{i}"] = asyncio.create_task(
                self._collect_news(news_params["news"], news_params["params"], news_params["condition"]))
        for i, news_params in enumerate(news_params_list):
            await name[f"task{i}"]


if __name__ == '__main__':
    c = Collection()
    c.collect_all_news([{"news": ChainNews, "params": ({"q": "btc"}), "condition": "all"},
                        {"news": ChainNews, "params": ({"q": "btc"}), "condition": "all"}])
    print(c.news_parser.news_dataframe)
