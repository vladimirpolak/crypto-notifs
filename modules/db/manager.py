from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from instagrapi.types import Comment

engine = create_engine('sqlite:///test_db.db', echo=True)
Base = declarative_base()


class CommentModel(Base):
    __tablename__ = "Comments"

    id = Column(Integer, primary_key=True)
    pk = Column(String)
    text = Column(String)
    # user = UserModelForeignKey
    created_at = Column(DateTime)
    content_type = Column(String)
    status = Column(String)

    def __init__(self, pk, text, created_at, content_type, status):
        self.pk = pk
        self.text = text
        self.created_at = created_at
        self.content_type = content_type
        self.status = status


Base.metadata.create_all(engine)