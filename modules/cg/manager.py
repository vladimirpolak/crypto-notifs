from pycoingecko import CoinGeckoAPI as CG
from modules.cg.models import Price, Coin
from collections import defaultdict
from typing import List


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

    def get_prices(self, coin_names: list, currencies: list) -> dict:
        """
        Fetches requested values of coins/currencies.

        :param coin_names: list('bitcoin', 'ethereum'...)
        :param currencies: list('usd', 'eur'...)
        :return: dict('coin_name': list[Price]}
        """
        r = self.get_price(
            ids=coin_names,
            vs_currencies=currencies
        )

        output = defaultdict(list)
        for coin, prices in r.items():
            for currency, value in prices.items():
                output[coin].append(
                    Price(
                        currency=currency,
                        value=value
                    )
                )

        return output
