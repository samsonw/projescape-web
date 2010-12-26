"""The application's model objects"""
from projescapeweb.model.meta import Session, Base

from projescapeweb.model.user import User, UserDetail


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)
