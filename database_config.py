from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database_uri = "mysql://root:toor2019@localhost:3306/sys"
engine = create_engine(database_uri)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()