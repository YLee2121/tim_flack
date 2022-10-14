import smtplib
from email.mime.text import MIMEText
from random import randint


class Email_server:
    
    def __init__(self):
        """
        define the email server
        gmail: bumarketplace488@gmail.com
        password: Admin2022@@
        App Password: grihtpchplddgqkv
        """
        self.email_user = "bumarketplace488"
        self.email_password ="grihtpchplddgqkv"

        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.server.ehlo()
        self.server.login(self.email_user, self.email_password)

    
    def create_mail_with_code(self, receiver_addr, code):
        subject = 'BU MarketPlace Notification'
        content = '''Hi {}, 

Your one time authedication code is {}
        
Best, 
BU MarketPlare Admin'''.format(receiver_addr, code)

        msg = MIMEText(content)
        msg['Subject'] = subject


        return msg.as_string()

    def send_email(self, receiver_addr, message):
        self.server.sendmail(self.email_user, receiver_addr, message)
        

    @staticmethod
    def code_generator():
        return randint(111111, 999999)
        



if __name__ == '__main__': 
    tom = 'kyleleey@bu.edu'
    tom1 = 'yi.lee.77890@gmail.com'
    tom3 = 'kylelee@gapp.nthu.edu.tw'
    s = Email_server()
    msg = s.create_mail_with_code(tom1, 33000)
    s.send_email(tom1, msg)