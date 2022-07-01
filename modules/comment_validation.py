import re


class CommentData:
    def __init__(self,
                 coin_symbol: str,
                 condition: str,
                 value: int,
                 currency: str
                 ):
        self.coin_symbol = coin_symbol
        self.condition = condition
        self.value = value
        self.currency = currency or None


def verify_comment(comment: str) -> re.Match:
    """
    Validates the input comment against the required formatting.

    :param comment: string
    :return: Match or None
    """
    pattern = re.compile("[a-z]+?[<>][0-9]+([a-z]+)?")
    match = re.match(pattern, comment)

    return match


def extract_data(comment) -> CommentData:
    """
    Used to extract data from comment.

    :return: CommentData class
    """
    pattern = re.compile("([a-z]+?)([<>])([0-9]+)([a-z]+)?")
    data = re.findall(pattern, comment)[0]
    return CommentData(
        coin_symbol=data[0],
        condition=data[1],
        value=data[2],
        currency=data[3]
    )


if __name__ == '__main__':
    comments = [
        "btc<20000",
        "btc>50000usd",
        "eth>3000",
        "This comment should not raise exception."
    ]
    for comm in comments:
        print(verify_comment(comm))
