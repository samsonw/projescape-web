"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password

from hashlib import md5 as _md5
from email.mime.text import MIMEText

from pylons import url, app_globals
from webhelpers.html.tags import *

def md5(text):
    digester = _md5()
    digester.update(text)
    return digester.hexdigest()

def gravatar(email, md5=True, size=None):
    email_md5 = email
    if md5:
        email_md5 = md5(email)
    base_url = "http://www.gravatar.com/avatar/%s" % email_md5
    if size is not None:
        return base_url + ("?s=%d" % size)
    else:
        return base_url

def sendmail(from_addr, to_addr, subject, content):
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr

    app_globals.smtp.sendmail(from_addr, [to_addr], msg.as_string())

def to_bool(s):
    return s.upper() == 'TRUE'

