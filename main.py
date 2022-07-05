from modules.comment_validation import verify_comment
from modules.cg.manager import CoinGecko
from modules.db.manager import Database
from modules.ig.manager import Instagram
from modules.exceptions import CommentValidationError
from pathlib import Path
import json

UPDATE_INSTA = False


class CryptoNotifs:
    def __init__(self,
                 coingecko: CoinGecko,
                 database: Database,
                 instagram: Instagram
                 ):
        self.cg = coingecko
        self.db = database
        self.ig = instagram
        self.requests = []

    def main(self):
        # If there are no coins in the database get info for all coins
        if not self.db.get_coins():
            self.init_coins()

        # TODO  instagram comments will have to be updated in a larger
        #       time periods than coin prices to avoid being flagged by IG.
        if UPDATE_INSTA:
            self.get_instagram_comments()

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
        cg_coins = self.cg.get_detailed_coins()

        for coin in cg_coins:

            # Add every coin and it's prices to database
            c = self.db.insert_new_coin(coin)
            for price in coin.price:
                self.db.insert_price(
                    coin=c,
                    new_price=price
                )
        pass

    def get_instagram_comments(self):
        """
        Get comments from the instagram post that holds targetted comments.
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
            except CommentValidationError as e:
                print(
                    e,
                    f"INVALID COMMENT {comment}\n"
                    f"Comment: {comment.text}"
                )
                # Append the comment for deletion
                to_remove.append(comment)

        if to_remove:
            self.ig.api.comment_bulk_delete(
                media_id=self.ig.api.media_id(post.pk),
                comment_pks=[c.pk for c in to_remove]
            )

    def update_coins(self):
        """
        Updates coins based on comment requests saved in database.
        """
        # Get all requested coins/currencies from database
        comments = self.db.get_all_comments()
        coins_requested = set([comment.coin.name for comment in comments])
        currencies_requested = set([comment.currency for comment in comments])

        # Request price for all coins
        data = self.cg.get_prices(
            coin_names=list(coins_requested),
            currencies=list(currencies_requested)
        )

        # Save updated prices to database
        for coin_name, prices in data.items():
            coin = self.db.get_coin(name=coin_name)
            for price in prices:
                self.db.insert_price(
                    coin=coin,
                    new_price=price
                )


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
