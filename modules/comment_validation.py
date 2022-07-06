import re


def verify_comment(comment: str) -> re.Match:
    """
    Validates the input comment against the required formatting.

    :param comment: string
    :return: Match or None
    """
    pattern = re.compile("[a-zA-Z]+?[<>][0-9]+([a-zA-Z.]+)?")
    match = re.match(pattern, comment)

    return match


def extract_data(comment) -> tuple:
    """
    Used to extract data from comment.

    :return: (coin_symbol, condition, target_value, currency)
    """
    pattern = re.compile("([a-zA-Z]+?)([<>])([0-9]+)([a-zA-Z.]+)?")
    data = re.findall(pattern, comment)[0]

    coin_symbol = data[0].lower()
    condition = data[1]
    target_value = float(data[2])
    currency = data[3].lower()

    return coin_symbol, condition, target_value, currency


if __name__ == '__main__':
    comments = [
        "btc<20000",
        "btc>50000usd",
        "eth>3000",
        "Eth>6000isd",
        "This comment should not raise exception."
    ]
    for comm in comments:
        print(verify_comment(comm))
