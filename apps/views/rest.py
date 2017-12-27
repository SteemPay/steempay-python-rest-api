from flask import Blueprint, jsonify
from pymarketcap import Pymarketcap

from helpers import get_steem_account, get_account_history


steem_rest = Blueprint('Steem', __name__)


@steem_rest.route("/<username>")
def get_user(username):
    account = get_steem_account(username)

    return jsonify(account)


@steem_rest.route("/<username>/history/<limit>")
def get_transaction_history(username, limit):
    history = get_account_history(username, limit)

    return jsonify(history)


@steem_rest.route("/<username>/value/")
def get_account_values(username):
    market = Pymarketcap()
    account = get_steem_account(username)

    steem_price = float(market.ticker("steem")["price_usd"])
    steem_dollar_price = float(market.ticker("steem-dollars")["price_usd"])

    steem_balance = account["balance"]
    steem_dollar_balance = account["sbd_balance"]
    savings_balance = account["savings_balance"]

    steem = float(steem_balance.split(" ")[0])
    steem_dollars = float(steem_dollar_balance.split(" ")[0])
    savings = float(savings_balance.split(" ")[0])

    total_price = steem * steem_price + steem_dollars * steem_dollar_price + savings * steem_price

    output = {
        "steem": {
            "amount": steem,
            "price_usd": steem * steem_price
        },
        "steem-dollars": {
            "amount": steem_dollars,
            "price_usd":  steem_dollars * steem_dollar_price
        },
        "savings": {
            "amount": savings,
            "price_usd":  savings * steem_price
        },
        "total":{
            "price_usd": total_price
        }
    }

    return jsonify(output)


@steem_rest.route("/<username>/history")
def get_transaction_history_all(username):
    history = get_account_history(username)

    return jsonify(history)


@steem_rest.route("/<username>/attribute/<attribute>")
def get_user_attribute(username, attribute):
    account = get_steem_account(username)

    if attribute in account.keys():
        return jsonify(account[attribute])
    else:
        return jsonify({})
