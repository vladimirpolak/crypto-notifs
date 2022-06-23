from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

btc_price = cg.get_price(ids='bitcoin', vs_currencies='usd')
print(btc_price)


def get_price(coin_id: str, currency: str = "usd") -> int:
    r = cg.get_price(ids=coin_id, vs_currencies=currency)
    return int(r[coin_id][currency])

# Multiple coins/currencies in one request
# cg.get_price(ids=["bitcoin", "ethereum"], vs_currencies=["usd", "eur"])

# Price of single coin
# price = get_price(
#     coin_id='bitcoin',
#     currency='usd'
# )

# coins_detailed = cg.get_coins() # Get detailed list of coins
#
# # coins = cg.get_coins_list() # Get basic list of coins
# for coin in coins_detailed:
#     print(coin["name"])