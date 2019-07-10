
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

class BlogModel(Base):

    __tablename__ = "blogs"

    blog_id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    author = Column(Integer)

    def __repr__(self):
        return "<BlogModel title: {} AuthorId: {} >".format(self.title, self.author)