class NotifyMeTemplate:
    notify_me_news_template = """
<p>亲爱的订阅者，您好！</p>
<p style='font-indent:2em'>以下是您订阅的新闻信息:</p>\n"""


class NotifyMe(NotifyMeTemplate):
    def __init__(self, news_dict: dict):
        self.news_dict = news_dict

    @property
    def notify_me_news(self):
        if self.news_dict:
            for key in self.news_dict:
                self.notify_me_news_template += f"<p style='text-indent:2em'><a href='{self.news_dict[key]}'>{key}</a></p>\n"
            return self.notify_me_news_template


if __name__ == '__main__':
    print(NotifyMe({"a": "a", "b":"b"}).notify_me_news)
