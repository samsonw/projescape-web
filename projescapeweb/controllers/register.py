import logging
import uuid
from datetime import datetime

from pylons import request, response, session, tmpl_context as c, url, app_globals as g
from pylons.controllers.util import abort, redirect
from pylons.decorators.rest import restrict

from projescapeweb.lib.base import BaseController, render, Session
from projescapeweb.lib.helpers import md5, sendmail
from projescapeweb.model.user import User

log = logging.getLogger(__name__)

class RegisterController(BaseController):

    def index(self):
        return render('register/index.html')

    def pending(self):
        return render('register/pending.html')

    def activate(self, id):
        username = g.redis.get(id)
        if username is None:
            c.success = False
        else:
            c.success = True
            user_q = Session.query(User)
            user = user_q.filter_by(username=username).first()
            if user is not None:
                user.active = True
                user.created_time = datetime.now()
                Session.add(user)
                Session.commit()
        return render('register/activate.html')
    
    @restrict('POST')
    def save(self):
        username = request.params['username']
        password = request.params['passwd']
        password_2 = request.params['passwd_2']
        email = request.params['email']

        if password != password_2:
            session['flash'] = 'Password missmatch' 
            redirect(url(controller='register', action='index'))
            return;

        user_q = Session.query(User)
        if user_q.filter_by(username=username).first() is not None:
            session['flash'] = 'Username obtained by others'
            redirect(url(controller='register', action='index'))
            return;

        ## create user and save
        user = User() 
        user.activate = False
        user.username = username
        user.email = email
        user.email_md5 = md5(email)
        user.password = md5(password)

        Session.add(user)
        Session.commit()

        ## store activation data
        activation_id = uuid.uuid1().hex
        g.redis.set(activation_id, username)
        g.redis.expire(activation_id, 1*24*60*60) # store the data for 1 day

        ## send activation email
        activation_link = g.url_root + url(controller='register', 
                action='activate', id=activation_id)
        c.activation_link = activation_link
        content = render('register/activation.email')
        sendmail('no-reply@projescape', email, 'Activation your account in Projescape', content)

        ## redirect user to information page
        session['user.email'] = email
        redirect(url(controller='register', action='pending'))

