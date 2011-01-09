import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from projescapeweb.lib.base import BaseController, render

log = logging.getLogger(__name__)

class PortalController(BaseController):

    def index(self):
        return render('/index.html')
