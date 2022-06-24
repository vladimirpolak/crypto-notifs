from sqlalchemy import ForeignKey, create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///test_db.db')
Base = declarative_base()


class UserModel(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    pk = Column(String)
    username = Column(String)
    fullname = Column(String)
    comments = relationship("CommentModel", back_populates="user")

    def __init__(self, pk, username, fullname):
        self.pk = pk
        self.username = username
        self.fullname = fullname


class CommentModel(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    pk = Column(String)
    text = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("UserModel", back_populates="comments")
    # created_at = Column(DateTime)
    # content_type = Column(String)
    # status = Column(String)

    def __init__(self, pk, text): # , created_at, content_type, status
        self.pk = pk
        self.text = text
        # self.created_at = created_at
        # self.content_type = content_type
        # self.status = status


class CoinModel(Base):
    __tablename__ = "coin"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String)
    prices = relationship("PriceModel", back_populates="coin")
    last_updated = Column(DateTime)

    def __init__(self, code, name):
        self.code = code
        self.name = name


class PriceModel(Base):
    __tablename__ = "price"

    id = Column(Integer, primary_key=True)
    coin_id = Column(Integer, ForeignKey("coin.id"))
    coin = relationship("CoinModel", back_populates="prices")
    currency = Column(String)
    price = Column(Integer)

    def __init__(self, currency, price):
        self.currency = currency
        self.price = price


if __name__ == '__main__':
    Base.metadata.create_all(engine)
