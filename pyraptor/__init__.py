from flask import Flask, request

from pyraptor.router import router

app = Flask(__name__)


@app.route("/healthcheck")
def healtcheck():
    return "OK"


@app.route("/route")
def get_route():
    origin_stop_id = request.args.get('origin_stop_id')
    dest_stop_id = request.args.get('dest_stop_id')

    return str(router.find_route(origin_stop_id, dest_stop_id))
