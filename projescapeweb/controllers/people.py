import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from projescapeweb.lib.base import BaseController, Session, render
from projescapeweb.model.user import User

log = logging.getLogger(__name__)

class PeopleController(BaseController):

    def home(self, id):
        if id is None and 'user.id' in session:
            id = session.get('user.id')

        if id is None:
            abort(404)
            return

        user_q = Session.query(User)
        user = user_q.filter_by(username=id).first()

        c.user = user

        return render('/people/home.html')

