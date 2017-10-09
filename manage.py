from flask_script import Manager, Server

from apps import steempay_api_app, steempay_socket

manager = Manager(steempay_api_app)

server = Server(host="0.0.0.0", port=9000, use_debugger=True, use_reloader=True)


# manager.add_command("run", server)

@manager.command
def run():
    steempay_socket.run(
        steempay_api_app,
        host='0.0.0.0',
        port=9000,
        use_reloader=True,
        use_debugger=True
    )


if __name__ == '__main__':
    manager.run()
