from sqlalchemy.orm import sessionmaker
from modules.db.db_tables import engine, CommentModel, UserModel
# https://stackoverflow.com/a/16434931

Session = sessionmaker(bind=engine)
session = Session()

# INSERTING A NEW USER
# user = UserModel(pk="314319841513519", username="John", fullname="John Doe")
# session.add(user)
# session.commit()

# QUERYING FOR A USER
# q = session.query(UserModel).filter_by(pk="314319841513519")
# user = q.first()

# INSERTING NEW COMMENT
# comment = CommentModel(
#     pk="1415901521512",
#     text="New comment",
# )
# user.comments.append(comment)
# session.commit()

# GETTING COMMENTS OF A USER
# print(user.comments[0].pk)


