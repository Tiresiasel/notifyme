import json

from module import ChainNews
from service import SendEmail, NotifyMe


class Main:
    def __init__(self):
        with open("config.json", "r") as f:
            self.keyword_list = json.load(f)["keyword_list"]
        cn = ChainNews("https://www.chainnews.com/", "search?")
        for keyword in self.keyword_list:
            cn.update_all_qualify_news({"q": keyword},"today")
        self.news_dict = cn.news_dict
        if self.news_dict:
            self.msg = NotifyMe(self.news_dict).notify_me_news
            self.se = SendEmail(self.msg)
        else:
            raise ValueError("当日没有新闻")

    def send_email(self, receiver: str):
        self.se.send_email(receiver)

    def send_emails(self, receiver_list: list = None):
        if receiver_list is not None:
            for receiver in receiver_list:
                self.se.send_email(receiver)
        else:
            self.send_emails()

if __name__ == '__main__':
    main = Main()
    main.send_email("1275021527@qq.com")