
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, TIMESTAMP

Base = declarative_base()


class BlogModel(Base):

    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    content = Column(String)
    author = Column(Integer)
    created_on = Column(TIMESTAMP)
    deleted_on = Column(TIMESTAMP)
    edited_on = Column(TIMESTAMP)

    def getDict(self):
        d = {
            'id': self.id,
            "name": self.name,
            "content": self.content,
            "author": self.author
        }
        return d

    def __repr__(self):
        return "<BlogModel title: {} AuthorId: {} >".format(self.name, self.author)
