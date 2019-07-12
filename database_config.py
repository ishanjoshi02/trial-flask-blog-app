from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DEBUG

database_uri = "mysql://root:toor2019@flaskdemoinstance.c0x127jnab22.ap-south-1.rds.amazonaws.com:3306/sys"
engine = create_engine(database_uri)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


def getConfig():
    if DEBUG:
        return {
            "HOST_NAME": 'flaskdemoinstance.c0x127jnab22.ap-south-1.rds.amazonaws.com',
            "USERNAME": "root",
            "PASSWORD": "toor2019",
            "DATABASE": "sys",
        }
