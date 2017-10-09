from flask import Blueprint, jsonify

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
