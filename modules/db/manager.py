from modules.db.tables import CommentModel, UserModel, CoinModel, PriceModel, Base
from sqlalchemy.orm import sessionmaker, Session
from instagrapi.types import Comment, UserShort
from modules.cg.models import Coin, Price
from pathlib import Path
from typing import List

from sqlalchemy import create_engine

# https://stackoverflow.com/a/16434931

db_name = "test_db.db"
db_path = Path().cwd() / db_name

engine = create_engine(f'sqlite:///{db_path}')  # dialect+driver://username:password@host:port/database


def create_db():
    Base.metadata.create_all(engine)


def my_session():
    s = sessionmaker(bind=engine)
    return s()


class Database:
    def __init__(self, session: Session = my_session()):
        self.session = session

        # Creates new database if one doesn't exist
        if not db_path.exists():
            create_db()

    # ----------------------- Users/Comments -----------------------
    def get_comment(self, pk, **kwargs) -> CommentModel:
        """
        Get single comment

        :param pk: str
            Unique identifier of a comment

        :return: CommentModel
            Class containing comment's information
        """
        return self.session.query(CommentModel).filter_by(pk=pk, **kwargs).first()

    def get_user(self, pk, **kwargs) -> UserModel:
        """
        Get single user

        :param pk: str
            Unique identifier of a user

        :return: UserModel
            Class containing user's information
        """
        return self.session.query(UserModel).filter_by(pk=pk, **kwargs).first()

    def get_all_comments(self) -> List[CommentModel]:
        """
        Used to fetch all comments from the database.

        :return: List of classes each containing comment information
        """
        return self.session.query(CommentModel).all()

    def get_all_users(self) -> List[UserModel]:
        """
        Used to fetch all users from the database.

        :return: List of classes each containing user information
        """
        return self.session.query(UserModel).all()

    # This method is called withing 'insert_comment' method
    # so it won't be called directly in most cases.
    def insert_user(self, new_user: UserShort) -> UserModel:
        """
        Used for inserting a user into database.

        :param new_user: UserShort
            (Instagrapi class)
        :return: UserModel
            class representing database entry
        """
        # Check if user is not already in the database
        user = self.get_user(pk=new_user.pk)

        if not user:
            # Create new user
            user = UserModel(
                pk=new_user.pk,
                username=new_user.username,
                fullname=new_user.full_name
            )
            self.session.add(user)
            self.session.commit()

        return user

    def insert_comment(self, new_comment: Comment) -> CommentModel:
        """
        Used for inserting a comment into database.

        :param new_comment: Comment
            (Instagrapi class)
        :return: CommentModel
            class representing database entry
        """
        # Check if user is not already in the database
        comm = self.get_comment(pk=new_comment.pk)

        if not comm:

            # Get comment's user
            user = self.insert_user(new_comment.user)

            # Create new comment
            comm = CommentModel(
                pk=new_comment.pk,
                text=new_comment.text,
                created_at=new_comment.created_at_utc,
                content_type=new_comment.content_type,
                status=new_comment.status
            )
            user.comments.append(comm)
            self.session.commit()

        return comm

    # ----------------------- Coins/Prices -----------------------
    def insert_new_coin(self, new_coin: Coin) -> CoinModel:
        """
        Used for inserting a new coin into database.

        :return: CoinModel
        """
        # Check if coin is not already in the database
        coin = self.get_coin(symbol=new_coin.symbol)

        if not coin:
            print(f"Inserting new coin: {new_coin.name}")
            # Create new coin
            coin = CoinModel(
                symbol=new_coin.symbol,
                name=new_coin.name,
            )
            self.session.add(coin)
            self.session.commit()

        return coin

    def insert_price(self, coin_symbol: str, new_price: Price) -> PriceModel:
        """
        Used for inserting/updating a coin price into database.

         :return: PriceModel
        """
        # Get the corresponding coin from the database
        coin = self.get_coin(symbol=coin_symbol)

        # Create new price's model
        price = PriceModel(
            currency=new_price.currency,
            value=new_price.value
        )

        # Update an existing price
        for p in coin.prices:
            if p.currency == price.currency:

                # If new price is same as the one already in database
                if p.value == price.value:
                    print(f"Price for {coin.name} didn't change. ({p.value}{p.currency})")
                    return p

                print(f"Updating price for {coin.name}: {p.value}{p.currency} -> {price.value}{price.currency}.")
                p.value = price.value
                self.session.commit()
                return p

        # Insert new price since it didn't exist already
        print(f"Inserting new price for {coin.name}: {price.value}{price.currency}.")
        coin.prices.append(price)
        self.session.commit()
        return price

    def get_coin(self, **kwargs) -> CoinModel:
        """
        Used to fetch a coin info from database.

        :return: CoinModel
        """
        return self.session.query(CoinModel).filter_by(**kwargs).first()

    def get_coins(self) -> List[CoinModel]:
        """
        Used to fetch a list of coins from database.

        :return: list of CoinModel classes
        """
        return self.session.query(CoinModel).all()


if __name__ == '__main__':
    db = Database()
