import smtplib
from email.mime.text import MIMEText


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

    def send_email(self, sender_id, receiver_addr, message):
        self.server.sendmail(sender_id, receiver_addr, message)
        


