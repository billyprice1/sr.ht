import smtplib
import pystache
import os
import html.parser
from email.mime.text import MIMEText
from werkzeug.utils import secure_filename
from flask import url_for

from srht.database import db
from srht.objects import User
from srht.config import _cfg, _cfgi

def send_invite(user):
    if _cfg("smtp-host") == "":
        return
    smtp = smtplib.SMTP(_cfg("smtp-host"), _cfgi("smtp-port"))
    smtp.login(_cfg("smtp-user"), _cfg("smtp-password"))
    with open("emails/invite") as f:
        message = MIMEText(html.parser.HTMLParser().unescape(\
            pystache.render(f.read(), {
                'user': user,
                "domain": _cfg("domain"),
                "protocol": _cfg("protocol")
            })))
    message['X-MC-Important'] = "true"
    message['X-MC-PreserveRecipients'] = "false"
    message['Subject'] = "Your u.pste.pw account is approved"
    message['From'] = "noreply@pste.pw"
    message['To'] = user.email
    smtp.sendmail("noreply@pste.pw", [ user.email ], message.as_string())
    smtp.quit()

def send_rejection(user):
    if _cfg("smtp-host") == "":
        return
    smtp = smtplib.SMTP(_cfg("smtp-host"), _cfgi("smtp-port"))
    smtp.login(_cfg("smtp-user"), _cfg("smtp-password"))
    with open("emails/reject") as f:
        message = MIMEText(f.read())
    message['X-MC-Important'] = "true"
    message['X-MC-PreserveRecipients'] = "false"
    message['Subject'] = "Your pste.pw account has been rejected"
    message['From'] = "noreply@pste.pw"
    message['To'] = user.email
    smtp.sendmail("noreply@pste.pw", [ user.email ], message.as_string())
    smtp.quit()

def send_reset(user):
    if _cfg("smtp-host") == "":
        return
    smtp = smtplib.SMTP(_cfg("smtp-host"), _cfgi("smtp-port"))
    smtp.login(_cfg("smtp-user"), _cfg("smtp-password"))
    with open("emails/reset") as f:
        message = MIMEText(html.parser.HTMLParser().unescape(\
            pystache.render(f.read(), {
                'user': user,
                "domain": _cfg("domain"),
                "protocol": _cfg("protocol"),
                'confirmation': user.passwordReset
            })))
    message['X-MC-Important'] = "true"
    message['X-MC-PreserveRecipients'] = "false"
    message['Subject'] = "Reset your pste.pw password"
    message['From'] = "noreply@pste.pw"
    message['To'] = user.email
    smtp.sendmail("noreply@pste.pw", [ user.email ], message.as_string())
    smtp.quit()
