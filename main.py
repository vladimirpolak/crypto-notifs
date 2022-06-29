from modules.cg.manager import CoinGecko
from modules.db.manager import Database
from modules.ig.manager import Instagram
from pathlib import Path
import json


class CryptoNotifs:
    def __init__(self, coingecko, database, instagram):
        self.cg = coingecko
        self.db = database
        self.ig = instagram

    def main(self):
        # get comments/users from post and save to db
        #   request first 12 posts
        #   request all comments of 1st post
        #   for every comment
        #       add user if is new
        #       verify comment
        #       [a-z]+?[<>][0-9]+?
        #       add comment to the user if is new

        # get prices of the requested coins in db + save prices to db
        #   get all requested prices from database
        #   request price for all coins
        #   add prices to database

        # check if any desired condition is met
        #   get all price requests from db
        #   check if any condition is met

        # if condition is met, notify the particular user through dm
        #   get comment's user
        #   get user's pk
        #   get existing thread for user or create new dm
        pass


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

    cn = CryptoNotifs(cg, db, ig)
