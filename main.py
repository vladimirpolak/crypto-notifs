from modules.comment_validation import verify_comment
from modules.cg.manager import CoinGecko
from modules.db.manager import Database
from modules.ig.manager import Instagram
from modules.exceptions import CommentValidationError
from pathlib import Path
import time
import json


class CryptoNotifs:
    def __init__(self, coingecko: CoinGecko,
                 database: Database,
                 instagram: Instagram
                 ):
        self.cg = coingecko
        self.db = database
        self.ig = instagram
        self.requests = []

    def main(self):
        # If there are no coins in the database
        if not self.db.get_coins():
            # Get info for all coins
            self.init_coins()

        # TODO  instagram comments will have to be updated in a larger
        #       time periods than coin prices to avoid being flagged by IG.
        # self.get_instagram_comments()

        self.update_coins()

        # check if any desired condition is met
        #   get all price requests from db
        #   check if any condition is met

        # if condition is met, notify the particular user through dm
        #   get comment's user
        #   get user's pk
        #   get existing thread for user or create new dm
        pass

    def init_coins(self):
        """
        Creates/Updates all currencies/coins.
        Used only for database initialization.
        After this we only update the coins/prices that users request
        in order to alleviate the CoinGecko API.
        """
        # Request detailed coins info from coingecko
        coins = self.cg.get_detailed_coins()

        for coin in coins:

            # Add every coin and it's prices to database
            self.db.insert_new_coin(coin)
            for price in coin.price:
                self.db.insert_price(
                    coin_symbol=coin.symbol,
                    new_price=price
                )
        pass

    def get_instagram_comments(self):
        """
        Get comments of an instagram post that holds targetted comments.
        """
        # Get first item of user's media (pinned post is first)
        post = self.ig.api.user_medias(self.ig.api.user_id)[0]
        # Extract comments
        comments = self.ig.api.media_comments(post.pk, amount=0)
        print(f"Fetched {len(comments)} comments.")

        to_remove = []
        for comment in comments:
            try:
                self.db.insert_user(comment.user)
                self.db.insert_comment(comment)
            except CommentValidationError:
                print(
                    f"INVALID COMMENT {comment}"
                    f"Comment: {comment.text}"
                )
                # Append the comment for deletion
                to_remove.append(comment)

        if to_remove:
            self.ig.api.comment_bulk_delete(
                media_id=self.ig.api.media_id(post.pk),
                comment_pks=[c.pk for c in comments]
            )

    def update_coins(self):
        # get prices of the requested coins in db + save prices to db

        #   add prices to database

        # Get all requested coins/currencies from database
        comments = self.db.get_all_comments()
        coins_requested = set([comment.coin for comment in comments])
        currencies_requested = set([comment.currency for comment in comments])

        # TODO Custom get_price method that returns list of Price Classes
         # Request price for all coins
        r = self.cg.get_price(
            ids=[coin.name for coin in coins_requested],
            vs_currencies=list(currencies_requested)
        )

        # TODO Save prices to database


if __name__ == '__main__':
    # CoinGecko API init
    cg = CoinGecko()

    # Database interface init
    db = Database()

    # Load instagram credentials
    try:
        ig_credentials = json.load(Path("credentials.json").open("r"))
    except FileNotFoundError:
        ig_credentials = None
    # Instagram API init
    ig = Instagram(**ig_credentials)

    crypto_notifs = CryptoNotifs(cg, db, ig)
    crypto_notifs.main()
