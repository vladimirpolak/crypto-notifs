from modules.cg.manager import CoinGecko
from modules.db.manager import Database
from modules.db.tables import CommentModel
from modules.ig.manager import Instagram
from modules.exceptions import CommentValidationError
from modules.message import create_message
from pathlib import Path
import time
import random
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

        comments_to_notify = self.compare_requests_prices()

        if comments_to_notify:
            for comment in comments_to_notify:
                self.send_message(comment)
                self.db.delete_comment(comment)

            print(f"Deleting comments: {comments_to_notify}")
            self.ig.api.comment_bulk_delete(
                media_id=self.ig.api.media_id(self.ig.api.get_target_post().pk),
                comment_pks=[comment.pk for comment in comments_to_notify]
            )

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

    def get_instagram_comments(self):
        """
        Get comments from the instagram post that holds targetted comments.
        """
        # Get first (pinned) post
        post = self.ig.api.get_target_post()

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

    def compare_requests_prices(self) -> list:
        """
        Checks user defined conditions against current coin prices/currencies.
        Returns comments that met the condition defined.

        :return: list(CommentModel)
        """
        comments = self.db.get_all_comments()

        to_notify = []
        for comment in comments:
            requested_currency = comment.currency

            # TODO Use/Convert 'coin.prices' as dictionary where we can select specific price based on currency
            #   in order to avoid looping through all prices.
            # https://stackoverflow.com/questions/11578070/sqlalchemy-instrumentedlist-object-has-no-attribute-filter
            for price in comment.coin.prices:
                if price.currency == requested_currency:
                    curr_coin_value = price.value
                    target_coin_value = comment.target_value
                    condition = comment.condition

                    if ((condition == ">"
                         and curr_coin_value > target_coin_value)
                            or (condition == "<"
                                and curr_coin_value < target_coin_value)):

                        to_notify.append(comment)
                        print(f"Condition MET: {comment.coin.name.upper()} "
                              f"{curr_coin_value}{price.currency} {condition} {target_coin_value}{comment.currency}\n"
                              f"Comment: {comment}\n"
                              f"User: {comment.user}")
        return to_notify

    def send_message(self, comment: CommentModel):
        """
        Used to send a direct message to a user on Instagram.
        :param comment: CommentModel
        :return:
        """
        msg = create_message(
            username=comment.user.fullname,
            coin_name=comment.coin.name,
            value=[price.value for price in comment.coin.prices if price.currency == comment.currency][0],
            currency=comment.currency
        )
        msg = msg + " You are getting this message because you requested coin tracking with CryptoNotifs."

        time.sleep(random.uniform(10, 15))  # TIMEOUT
        self.ig.api.direct_send(
            text=msg,
            user_ids=[comment.user.pk]
        )
        print(f"Message sent. {comment}")
        time.sleep(random.uniform(4, 7))  # TIMEOUT


if __name__ == '__main__':
    # CoinGecko API init
    cg = CoinGecko()

    # Database interface init
    db = Database()

    # Instagram API init
    try:
        # Load instagram credentials
        ig_credentials = json.load(Path("credentials.json").open("r"))
    except FileNotFoundError:
        ig = Instagram()
    else:
        ig = Instagram(**ig_credentials)

    crypto_notifs = CryptoNotifs(cg, db, ig)
    crypto_notifs.main()
