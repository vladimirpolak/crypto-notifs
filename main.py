from modules.comment_validation import verify_comment
from modules.cg.manager import CoinGecko
from modules.db.manager import Database
from modules.ig.manager import Instagram
from pathlib import Path
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

        print(self.all_requests)
        exit()

        # TODO  instagram comments will have to be updated in a larger
        # TODO  time periods than coin prices to avoid being flagged by IG.
        self.get_instagram_comments()

        # get prices of the requested coins in db + save prices to db
        #   get all requested prices from database
        #   request price for all coins
        #   add prices to database
        comments = self.db.get_all_comments()

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
        # Get first item of user's media (pinned post is first)
        post = self.ig.api.user_medias(self.ig.api.user_id)[0]
        # Extract comments
        comments = self.ig.api.media_comments(post.pk, amount=0)
        print(f"Fetched {len(comments)} comments.")

        for comment in comments:
            # Validate comment
            comm_info = verify_comment(comment.text)

            # If valid, add comment/user to database
            if comm_info:
                self.db.insert_user(comment.user)
                self.db.insert_comment(comment)

    @property
    def all_requests(self) -> list:
        comments = self.db.get_all_comments()
        return [verify_comment(comment.text) for comment in comments]


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
