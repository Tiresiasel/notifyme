import datetime
import json
import logging
import smtplib
from email.mime.text import MIMEText

logging.getLogger().setLevel(logging.INFO)

class SendEmail:
    def __init__(self, content: str):
        self.message = MIMEText(content, 'html', 'utf-8')
        with open("config.json", "r") as f:
            self.config = json.load(f)
        self.receiver_list = self.config["receiver_list"]
        self.sender = self.config["sender"]
        self.smtp_host = self.config["smtp_host"]
        self.smtp_password = self.config["smtp_password"]
        self.message["From"] = self.config["from_header"]
        self.message["To"] = self.config["to_header"]
        self.message["Subject"] = self.config["subject"] + datetime.datetime.today().strftime("%Y-%m-%d")

    def send_email(self, receiver):
        try:
            smtp_obj = smtplib.SMTP()
            smtp_obj.connect(self.smtp_host,587) #网页smtp端口号
            smtp_obj.login(self.sender, self.smtp_password)
            smtp_obj.sendmail(self.sender, receiver, self.message.as_string())
            logging.info("邮件发送成功")
        except smtplib.SMTPException:
            logging.error("无法发送邮件")

    def send_emails(self):
        for receiver in self.receiver_list:
            self.send_email(receiver)

if __name__ == '__main__':
    SendEmail("a").send_email("1275021527@qq.com")
