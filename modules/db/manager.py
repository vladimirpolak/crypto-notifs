from sqlalchemy.orm import sessionmaker
from instagrapi.types import Comment, UserShort
from modules.db.db_tables import engine, CommentModel, UserModel
# https://stackoverflow.com/a/16434931

Session = sessionmaker(bind=engine)
session = Session()

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


class Database:
    def __init__(self, session):
        self.session = session

    def insert_user(self, new_user: UserShort):
        user = self.session.query(UserModel).filter_by(pk=new_user.pk).first()
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

    def insert_comment(self, new_comment: Comment):
        comm = self.session.query(CommentModel).filter_by(pk=new_comment.pk).first()
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
