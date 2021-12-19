# -*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import yaml

with open(r'config.yaml') as mail_config:
    config = yaml.load(mail_config, Loader=yaml.FullLoader)
server_login, server_password = config.get('config').get('mail_config')
class Mail():

    """
    Ах, если бы было не в падлу писать описания
    """

    def __init__(self, topic, text, addr_to):
        self.topic = topic
        self.text = text
        self.addr_to = addr_to

    def send_mail(self):
        msg = MIMEMultipart('alternative')  # Создаем сообщение
        msg['From'] = 'pvnuroms@mail.ru'  # от кого
        msg['To'] = self.addr_to  # Получатель
        msg['Subject'] = self.topic  # Тема сообщения
        msg.attach(MIMEText(f'Добрый день\n\n{self.text}', 'plain'))
        server = smtplib.SMTP('smtp.mail.ru', 587)  # Создаем объект SMTP
        server.starttls()
        server.login(server_login, server_password)
        server.set_debuglevel(True)  # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
        server.send_message(msg)  # Отправляем сообщение
        server.quit()

# TestZone
if __name__ == "__main__":
    mail = Mail('Тема', '\nКупи слона', f'{server_login},')
    mail.send_mail()

