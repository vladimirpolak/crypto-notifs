import re


def verify_comment(comment: str) -> tuple:
    """

    :param comment: string
    :return: tuple (crypto_coin_symbol,
                    condition (</>),
                    target_value,
                    currency (optional, None if not specified)
    """
    pattern = re.compile("([a-z]+?)([<>])([0-9]+)([a-z]+)?")
    match = re.match(pattern, comment)

    if not match:
        return None

    # Extract values
    coin_symbol = match.group(1)
    condition = match.group(2)
    value = int(match.group(3))
    currency = match.group(4)
    return coin_symbol, condition, value, currency


if __name__ == '__main__':
    comments = [
        "btc<20000",
        "btc>50000usd",
        "eth>3000",
        "This comment should not raise exception."
    ]
    for comm in comments:
        print(verify_comment(comm))
