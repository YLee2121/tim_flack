from flask_mail import Message
from . import mail_server, db
from random import randint


class email_cls:
    """
        define the email server
        gmail: bumarketplace488@gmail.com
        password: Admin2022@@
        App Password: grihtpchplddgqkv
     """

    @staticmethod
    def send_mail(receiver):
        code = email_cls.code_generator()
        msg = email_cls.create_mail_with_code(receiver, code)
        email_cls.update_db(receiver, code)
        mail_server.send(msg)

    @staticmethod
    def code_generator():
        return randint(111111, 999999)

    @staticmethod
    def update_db(email, code):
         # update or insert into the db
        c = {
            'email':email, 
            'code':code
            }

        if not db.email_to_code.find_one({"email":email}):
            db.email_to_code.insert_one(c)
        else:
            query_filter = {'email':email}
            new_val = { "$set": c}
            db.email_to_code.update_one(query_filter, new_val)


    @staticmethod
    def create_mail_with_code(receiver, code):
        msg = Message('BU MarketPlace Admin - noreply', sender = 'bumarketplace488@gmail.com', recipients = [receiver])
        msg.body = '''Hi {}, 

Your one time authendication code is {}

For first time signup, please check your "SPAM" box.

Best, 
BU MarketPlace'''.format(receiver, code)
        return msg