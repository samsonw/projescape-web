from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String, DateTime, PickleType, Boolean

from projescapeweb.model.meta import Base

class User(Base):
    """the user model, for user authentication"""

    __tablename__ = 'user'

    _id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password = Column(String(64))
    email = Column(String(32))
    email_md5 = Column(String(64))
    open_id = Column(String(128))
    open_id_alt = Column(String(128))
    created_time = Column(DateTime())
    active = Column(Boolean())
    user_detail_id = Column(Integer, ForeignKey("user_detail._id"))
    user_detail = relationship("UserDetail")

    def __init__(self):
        pass
        
class UserDetail(Base):
    """the user detail model, detail information"""

    __tablename__ = 'user_detail'

    _id = Column(Integer, primary_key=True)
    last_login = Column(DateTime())
    display_name = Column(String(length=32, convert_unicode=True))
    job_title = Column(String(length=128, convert_unicode=True))
    description = Column(String(length=256, convert_unicode=True))
    location = Column(String(length=64, convert_unicode=True))
    web_site = Column(String(length=64))
    social_links = Column(PickleType())

    def __init__(self):
        pass 

