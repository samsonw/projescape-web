import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.i18n import _
from pylons.controllers.util import abort, redirect
from pylons.decorators.rest import restrict

from projescapeweb.lib.base import BaseController, Session, render
from projescapeweb.lib.helpers import md5, gravatar
from projescapeweb.model.user import User

log = logging.getLogger(__name__)

class LoginController(BaseController):

    def index(self):
        return render('/login/index.html')

    @restrict('POST')
    def login(self):
        login = request.params['login']
        passwd = request.params['passwd']

        passwd_md5 = md5(passwd)

        user = None
        user_q = Session.query(User)
        if login.find('@') > 0:
            ## login with email
            email = login
            user = user_q.filter_by(email=email, password=passwd_md5).first()
        else:
            ## login with user id
            username = login
            user = user_q.filter_by(username=username, password=passwd_md5).first()

        if user is not None:
            if user.active:
                session['user.id'] = user.username
                avatar_url = gravatar(user.email_md5, md5=False, size=24)
                session['user.avatar'] = avatar_url
                redirect(url(controller='people', action='home', id=user.username))
                return 
            else:
                session['user.email'] = user.email
                redirect(url(controller='register', action='pending'))
        else:
            session['flash'] = _('Invalid login')
            redirect(url(controller='login', action='index'))

    def logout(self):
        session.delete()
        redirect('/')

    def openid(self):
        return 'test'
