from steem import Steem, account


def normalize(username):
    return str(username).lower()


def get_steem_account(username):
    username = normalize(username)

    steem_client = Steem()

    account = steem_client.get_account(username)

    return account


def stream_account_history(username, limit=None):
    username = normalize(username)

    steem_account = account.Account(username)

    if limit is not None:
        history = steem_account.history_reverse(batch_size=limit)
    else:
        history = steem_account.history_reverse()

    for item in history:
        if item["type"] == "transfer":
            yield item


def get_account_history(username, limit=None):
    output = []

    for item in stream_account_history(username, limit):
        output.append(item)

    return output
