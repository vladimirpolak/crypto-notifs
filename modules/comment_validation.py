import re


def verify_comment(comment: str) -> tuple:
    """
    Validates the input comment against the required formatting.

    :param comment: string
    :return: Match or None
    """
    pattern = re.compile("[a-z]+?[<>][0-9]+([a-z]+)?")
    match = re.match(pattern, comment)

    return match


def extract_data(comment) -> tuple:
    """
    Used to extract data from comment.

    :return: (coin_symbol, condition, target_value, currency(Optional))
    """
    pattern = re.compile("([a-z]+?)([<>])([0-9]+)([a-z]+)?")
    return re.findall(pattern, comment)[0]


if __name__ == '__main__':
    comments = [
        "btc<20000",
        "btc>50000usd",
        "eth>3000",
        "This comment should not raise exception."
    ]
    for comm in comments:
        print(verify_comment(comm))
