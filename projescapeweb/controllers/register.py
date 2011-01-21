import logging
import uuid
from datetime import datetime

from pylons import request, response, session, tmpl_context as c, url, app_globals as g, config
from pylons.i18n import _
from pylons.controllers.util import abort, redirect
from pylons.decorators.rest import restrict

from sqlalchemy import or_
from recaptcha.client import captcha

from projescapeweb.lib.base import BaseController, render, Session
from projescapeweb.lib.helpers import md5, sendmail, to_bool
from projescapeweb.model.user import User

log = logging.getLogger(__name__)

class RegisterController(BaseController):

    def index(self):
        c.enable_captcha = to_bool(config['recaptcha.enable'])
        c.pubkey = config['recaptcha.public']
        return render('register/index.html')

    def pending(self):
        if 'user.email' not in session:
            abort(403)
            return
        return render('register/pending.html')

    def reconfirm(self):
        email = session['user.email']
        if email is None:
            abort(403)
            return

        ## store activation data
        activation_id = uuid.uuid1().hex
        g.redis.set(activation_id, email)
        g.redis.expire(activation_id, 1*24*60*60) # store the data for 1 day

        ## send activation email
        activation_link = g.url_root + url(controller='register', 
                action='activate', id=activation_id)
        c.activation_link = activation_link
        content = render('register/activation.email')
        ## TODO maybe better to do it in background
        sendmail('no-reply@projescape', email, _('Activate your account in Projescape'), content)

        session['flash'] =  _('Confirmation email has been sent to you.')
        redirect(url(controller='register', action='pending'))

    def activate(self, id):
        email = g.redis.get(id)
        if email is None:
            c.success = False
        else:
            c.success = True
            user_q = Session.query(User)
            user = user_q.filter_by(email=email).first()
            if user is not None:
                user.active = True
                user.created_time = datetime.now()
                Session.add(user)
                Session.commit()
        return render('register/activate.html')
    
    @restrict('POST')
    def save(self):
        ## check captcha
        if to_bool(config['recaptcha.enable']) and 'register.disable_captcha' not in session:
            r = captcha.submit(request.params['recaptcha_challenge_field'],
                    request.params['recaptcha_response_field'],
                    config['recaptcha.private'],
                    request.environ['REMOTE_ADDR'])
            if not r.is_valid:
                session['flash'] = _('Invalid captcha')
                redirect(url(controller='register', action='index'))
                return;

        username = request.params['username']
        email = request.params['email']

        if 'register.disable_password' not in session:
            password = request.params['passwd']
            password_2 = request.params['passwd_2']

            if password != password_2:
                session['flash'] = _('Password missmatch')
                redirect(url(controller='register', action='index'))
                return;
        else:
            ## openid register
            password = None

        user_q = Session.query(User)
        if user_q.filter(or_(User.username==username, User.email==email)).first() is not None:
            session['flash'] = _('Username/Email obtained by others')
            redirect(url(controller='register', action='index'))
            return;

        ## create user and save
        user = User() 
        user.activate = False
        user.username = username
        user.email = email
        user.email_md5 = md5(email)
        user.password = None if password is None else md5(password)

        Session.add(user)
        Session.commit()

        ## redirect user to information page
        session['user.email'] = email

        ## store activation data
        activation_id = uuid.uuid1().hex
        g.redis.set(activation_id, email)
        g.redis.expire(activation_id, 1*24*60*60) # store the data for 1 day

        ## send activation email
        activation_link = g.url_root + url(controller='register', 
                action='activate', id=activation_id)
        c.activation_link = activation_link
        content = render('register/activation.email')
        ## TODO maybe better to do it in background
        sendmail('no-reply@projescape', email, _('Activate your account in Projescape'), content)

        session['flash'] =  _('Confirmation email has been sent to you.')
        redirect(url(controller='register', action='pending'))

    def reset(self, id=None):
        ## neither reset password nor modify password
        if id is None and 'user.id' not in session:
            abort(403)
            return

        if id is not None:
            email = g.redis.get(id)
            if email is not None:
                c.email = email
                session['register.require_password'] = False
            else:
                abort(403)
                return 
        else:
            session['register.require_password'] = True
            
        return render('register/reset.html')

    @restrict('POST')
    def save_password(self):
        if 'register.require_password' not in session:
            abort(403)
            return

        password = request.params['passwd']
        password_2 = request.params['passwd2']
        if password != password_2:
            session['flash'] = _('Password missmatch')
            redirect(url(controller='register', action='reset'))
            return;
        
        user_q = Session.query(User)
        if session['register.require_password']:
            username = session['user.id']
            old_password = md5(request.params['old_passwd'])

            user = user_q.filter_by(username=username, password=old_password).first()
            if user is None:
                session['flash'] = _('Invalid password')
                redirect(url(controller='register', action='reset'))
                return;
                
        else:
            user = user_q.filter_by(email=email).first()
            if user is None:
                session['flash'] = _('Invalid email')
                redirect(url(controller='register', action='reset'))
                return;

        user.password = md5(password)
        Session.add(user)
        Session.commit()


        session['flash'] = _('Password updated')
        redirect(url(controller='people', action='home', id=user.username))

