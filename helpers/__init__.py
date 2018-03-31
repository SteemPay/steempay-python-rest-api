from datetime import datetime, timedelta

from steem import Steem, account


def normalize(username):
    return str(username).lower()


def get_steem_account(username):
    username = normalize(username)

    steem_client = Steem()

    account = steem_client.get_account(username)

    return account


def stream_account_history(username):
    steem_account = account.Account(username)
    history = steem_account.history_reverse()

    for item in history:
        if item["type"] == "transfer":
            yield item


def stream_account_history_slow(username, since_date=None):
    from beem import account
    username = normalize(username)
    fmt = "%Y-%m-%dT%H:%M:%S"
    steem_account = account.Account(username)

    since_date = datetime.now() - timedelta(days=120)
    started = datetime.now()
    print(f"started at {started}")
    history = steem_account.history(start=since_date)

    for item in history:
        if item["type"] == "transfer":
            yield item

    print(f"Ended at {datetime.now()}\n {datetime.now() - started}")


def get_account_history(username):
    output = []

    for item in stream_account_history(username):
        if item not in output:
            output.append(item)

    return output
