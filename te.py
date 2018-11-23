from flask_mail import Message
from app import app, mail
import os

msg = Message("Test2",
              sender=os.getenv('EMAIL_USER'),
              recipients=["irshkur@gmail.com"],
              body="The email confirmation should contain a unique URL"
              )

with app.app_context():
    mail.send(msg)
# try:
#     mail.send(msg)
# except:
#     print('Email didnt send')

# except AssertionError as error:
#     print(error)
    # print('Email didn;t send')