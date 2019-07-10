
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    password = Column(String)

    is_authenticated=True
    is_active=True
    is_anonymous=True

    def get_id(self):
       
        return str(self.user_id).encode("utf-8").decode("utf-8")

    def __repr__(self):
        return "<UserModel username: {} name:{}>".format(self.username, self.name)