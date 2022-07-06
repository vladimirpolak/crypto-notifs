from random import choice

# [greeting] [username] [coin_name] [action] [value] [currency]

templates = [
    "%g %u, %C%a %v %c!",
    "%g, %C%a %v %c!"
]

greetings = [
    "Hi",
    "Hi there",
    "Hello",
    "Greetings",
    "Beware"
]
actions = [
    " just reached the value of",
    " is now valued at",
    " reached",
    "'s value is now",
    "'s value reached"
]


def create_message(
        username: str,
        coin_name: str,
        value: float,
        currency: str
):
    return choice(templates).replace(
        "%g", choice(greetings)
    ).replace(
        "%u", username
    ).replace(
        "%C", coin_name.title()
    ).replace(
        "%a", choice(actions)
    ).replace(
        "%v", str(value)
    ).replace(
        "%c", currency.upper()
    )


if __name__ == '__main__':
    msg = create_message(
        username="Username",
        coin_name="bitcoin",
        value=19783.4,
        currency="eur"
    )
    print(msg)
