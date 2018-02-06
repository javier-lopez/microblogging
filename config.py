import os
import urllib.parse

class Config(object):
    #general settings
    APP_ADMINS = os.environ.get('APP_ADMINS') or 'm@javier.io'
    APP_ADMINS = APP_ADMINS.split()
    APP_FROM   = os.environ.get('APP_ADMINS') or 'no-reply@microblogging.tld'

    #pagination
    PAGINATION_SETTINGS = {
        'items_per_page': 7,
    }

    #flask-wtf
    SECRET_KEY  = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    #flask-mongoengine
    MONGODB_HOST     = os.environ.get('MONGODB_HOST')     or 'mongodb'
    MONGODB_TCP_PORT = os.environ.get('MONGODB_TCP_PORT') or 27017
    MONGODB_TCP_PORT = int(MONGODB_TCP_PORT)
    MONGODB_DB       = os.environ.get('MONGODB_DB')       or 'microblogging'
    MONGODB_USER     = os.environ.get('MONGODB_USER')     or 'microblogging'
    MONGODB_PASSWD   = os.environ.get('MONGODB_PASSWD')   or 'microblogging'

    MONGODB_USER     = urllib.parse.quote_plus(MONGODB_USER)
    MONGODB_PASSWD   = urllib.parse.quote_plus(MONGODB_PASSWD)

    MONGODB_SETTINGS = {
        'db':       MONGODB_DB,
        'host':     MONGODB_HOST,
        'port':     MONGODB_TCP_PORT,
        'username': MONGODB_USER,
        'password': MONGODB_PASSWD,
    }

    #flask-mail
    SMTP_SERVER     = os.environ.get('SMTP_SERVER')     or 'smtp.mailgun.org'
    SMTP_TCP_PORT   = os.environ.get('SMTP_TCP_PORT')   or 587
    SMTP_TCP_PORT   = int(SMTP_TCP_PORT)
    SMTP_USER       = os.environ.get('SMTP_USER')       or 'sender@microblogging.tld'
    SMTP_PASSWD     = os.environ.get('SMTP_PASSWD')     or 'you-will-never-guess'
    SMTP_MAX_EMAILS = os.environ.get('SMTP_MAX_EMAILS') or 1000
    SMTP_MAX_EMAILS = int(SMTP_MAX_EMAILS)

    SMTP_SETTINGS = {
        'host':       SMTP_SERVER,
        'port':       SMTP_TCP_PORT,
        'username':   SMTP_USER,
        'password':   SMTP_PASSWD,
        'max_emails': SMTP_MAX_EMAILS,
    }

    MAIL_SERVER         = SMTP_SETTINGS['host']
    MAIL_PORT           = SMTP_SETTINGS['port']
    MAIL_USERNAME       = SMTP_SETTINGS['username']
    MAIL_PASSWORD       = SMTP_SETTINGS['password']
    MAIL_MAX_EMAILS     = SMTP_SETTINGS['max_emails']
    MAIL_DEFAULT_SENDER = APP_FROM
    #MAIL_DEBUG         = True
