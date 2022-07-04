from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


Base = declarative_base()


class UserModel(Base):
    """Instagram user model."""
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
    """Instagram comment model."""
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    pk = Column(String)
    text = Column(String)

    # Data extracted from comment
    coin_id = Column(Integer, ForeignKey("coin.id"))
    coin = relationship("CoinModel", back_populates="comments")
    condition = Column(String)
    target_value = Column(Float)
    currency = Column(String)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("UserModel", back_populates="comments")
    created_at = Column(DateTime)
    content_type = Column(String)
    status = Column(String)

    def __init__(self,
                 pk,
                 text,
                 coin,
                 condition,
                 target_value,
                 currency,
                 created_at,
                 content_type,
                 status
                 ):
        self.pk = pk
        self.text = text
        self.coin = coin
        self.condition = condition
        self.target_value = target_value
        self.currency = currency or "usd" # Setting default currency 'usd'
        self.created_at = created_at
        self.content_type = content_type
        self.status = status


class CoinModel(Base):
    """Crypto coin model."""
    __tablename__ = "coin"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True)
    name = Column(String, unique=True)
    prices = relationship("PriceModel", back_populates="coin")
    comments = relationship("CommentModel", back_populates="coin")

    def __init__(self, symbol, name):
        self.symbol = symbol
        self.name = name


class PriceModel(Base):
    """Crypto coin's price model."""
    __tablename__ = "price"

    id = Column(Integer, primary_key=True)
    coin_id = Column(Integer, ForeignKey("coin.id"))
    coin = relationship("CoinModel", back_populates="prices")
    currency = Column(String)
    value = Column(Float)
    last_updated = Column(DateTime)

    def __init__(self, currency, value):
        self.currency = currency
        self.value = value
