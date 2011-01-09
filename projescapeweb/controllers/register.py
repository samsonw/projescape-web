import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators.rest import restrict

from projescapeweb.lib.base import BaseController, render

log = logging.getLogger(__name__)

class RegisterController(BaseController):

    def index(self):
        return render('register/index.html')

    
    @restrict('POST')
    def save(self):
        ##TODO
