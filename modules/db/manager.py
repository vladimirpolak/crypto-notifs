from sqlalchemy.orm import sessionmaker, Session
from instagrapi.types import Comment, UserShort
from modules.cg.models import Coin, Price
from typing import List
from modules.db.tables import engine, CommentModel, UserModel, CoinModel, PriceModel
# https://stackoverflow.com/a/16434931

# INSERTING A NEW USER
# user = UserModel(pk="314311414519", username="John", fullname="John Doe")
# session.add(user)
# session.commit()

# QUERYING FOR A USER
# user = session.query(UserModel).filter_by(pk="124").first()
# print(user.fullname)

# INSERTING NEW COMMENT
# comment = CommentModel(
#     pk="4109",
#     text="Novy Koment",
# )
# user.comments.append(comment)
# session.commit()

# GETTING COMMENTS OF A USER
# print(user.comments[0].pk)
# print(session.query(CommentModel).filter_by(pk="4109").first().user.username)
# print(session.query(CommentModel).all())


def my_session():
    s = sessionmaker(bind=engine)
    return s()


class Database:
    def __init__(self, session: Session = my_session()):
        self.session = session

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
                # created_at=new_comment.created_at_utc,
                # content_type=new_comment.content_type,
                # status=new_comment.status
            )
            user.comments.append(comm)
            self.session.commit()

        return comm

    # ----------------------- Coins/Prices -----------------------
    def insert_new_coin(self, new_coin) -> CoinModel:
        """
        Used for inserting a new coin into database.

        :return: CoinModel
        """
        # Check if coin is not already in the database
        coin = self.get_coin(symbol=new_coin.symbol)

        if not coin:
            # Create new user
            coin = CoinModel(
                symbol=new_coin.symbol,
                name=new_coin.name,
            )
            self.session.add(coin)
            self.session.commit()

        return coin

    def insert_price(self, coin_symbol: str, price: int, currency: str) -> PriceModel:
        """
        Used for inserting/updating a coin price into database.

         :return: PriceModel
        """
        pass

    def get_coin(self, symbol, **kwargs) -> CoinModel:
        """
        Used to fetch a coin info from database.

        :return: CoinModel
        """
        pass

    def get_coins(self) -> List[CoinModel]:
        """
        Used to fetch a list of coins from database.

        :return: list of CoinModel classes
        """
        pass

    # def get_coin_price(self):
    #     """
    #     Used to fetch a coin's price from database.
    #
    #     :return: PriceModel
    #     """
    #     pass


if __name__ == '__main__':
    db = Database()
