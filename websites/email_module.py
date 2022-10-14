from flask_mail import Message
from . import mail_server
from random import randint

class email_cls:
    """
        define the email server
        gmail: bumarketplace488@gmail.com
        password: Admin2022@@
        App Password: grihtpchplddgqkv
     """

    @staticmethod
    def send_mail(msg):
        mail_server.send(msg)
    



    @staticmethod
    def code_generator():
        return randint(111111, 999999)


    @staticmethod
    def create_mail_with_code(receiver, code):
        msg = Message('BU MarketPlace Admin - noreply', sender = 'bumarketplace488@gmail.com', recipients = [receiver])
        msg.body = '''Hi {}, 

Your one time authendication code is {}

For first time signup, please check your "SPAM" box.

Best, 
BU MarketPlace'''.format(receiver, code)
        return msg