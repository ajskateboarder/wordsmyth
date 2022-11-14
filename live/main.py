from flask import Flask, Response, render_template
from helpers import format_sse, MessageAnnouncer


app = Flask(__name__)
announcer = MessageAnnouncer()


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/update')
def ping(data):
    msg = format_sse(data)
    announcer.announce(msg)
    return {}, 200


@app.route('/listen', methods=['GET'])
def listen():
    def stream():
        messages = announcer.listen()
        while True:
            msg = messages.get()
            yield msg

    return Response(stream(), mimetype='text/event-stream')