from pycoingecko import CoinGeckoAPI as CG
from modules.cg.models import Price, Coin
from typing import List


# btc_price = cg.get_price(ids='bitcoin', vs_currencies='usd')
# print(btc_price)


# def get_price(coin_id: str, currency: str = "usd") -> int:
#     r = cg.get_price(ids=coin_id, vs_currencies=currency)
#     return int(r[coin_id][currency])

# Multiple coins/currencies in one request
# coins = cg.get_price(ids=["bitcoin", "ethereum"], vs_currencies=["usd", "eur"])
# print(coins)

# Price of single coin
# price = get_price(
#     coin_id='bitcoin',
#     currency='usd'
# )


class CoinGecko(CG):
    def get_detailed_coins(self) -> List[Coin]:
        """
        Returns list of coins with their current market prices.
        Will be used to initializing database as after that we will
        only get prices for requested coins and update their prices accordingly.

        :return: List of Coin classes
        """
        coins_detailed = self.get_coins() # Get detailed list of coins

        output = []
        for coin in coins_detailed:
            price_data = coin["market_data"]["current_price"]
            price = [Price(currency=currency, value=value) for currency, value in price_data.items()]
            coin = Coin(
                name=coin["id"],
                symbol=coin["symbol"],
                price=price
            )
            output.append(coin)

        return output


# coins = cg.get_coins_list() # Get basic list of coins
