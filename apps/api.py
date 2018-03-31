from asyncio import Lock

from flask import Flask, session
import json

from apps.views import steem_rest
from flask_socketio import SocketIO, emit

from helpers import get_account_history

app = Flask(__name__)

app.register_blueprint(steem_rest)

socket = SocketIO(app)

thread = None
thread_lock = Lock()

NAMESPACE = '/history'


@app.route("/favicon.ico")
def favicon():
    return "", 204


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0

    while True:
        socket.sleep(10)
        count += 1

        emit(
            {
                "data": 'Server generated event'
            }
        )


def emit(data, broadcast=False):
    """
    Sends data to socketio
    :param bool broadcast: To broadcast or not to broadcast, that is the question
    :param dict data: dict of data to send
    :return: None
    """
    print("sending data {}".format(data))

    socket.emit(
        "history_event",
        data,
        broadcast=broadcast,
        namespace=NAMESPACE
    )


@socket.on('history', namespace=NAMESPACE)
def get_history(data):

    session['receive_count'] = session.get('receive_count', 0) + 1

    history = {}
    username = ""

    if "username" in data:
        username = data["username"]

        if "limit" in data.keys():
            history = get_account_history(username, data["limit"])
        else:
            history = get_account_history(username)

    data = {
        'username': username,
        'data': json.dumps(history),
        'count': session['receive_count']
    }

    emit(data, True)


@socket.on('connect', namespace=NAMESPACE)
def test_connect():
    print("Client connected")

    data = {
        'data': 'Connected'
    }

    emit(data)


@socket.on('disconnect', namespace=NAMESPACE)
def test_disconnect():
    print('Client disconnected')
