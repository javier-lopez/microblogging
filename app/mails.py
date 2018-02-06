from flask import render_template
from flask_mail import Message
from app import app, mail
from app.decorators import async

@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, text_body, html_body):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # mail.send(msg) #syncronized
    send_async_email(app,msg)

def email_follower_notification(follower, followed):
    send_email("[cbien] %s te esta siguiendo" % follower.username,
               [followed.email],
               render_template("follower_email.txt.j2",  user=followed, follower=follower),
               render_template("follower_email.html.j2", user=followed, follower=follower))
