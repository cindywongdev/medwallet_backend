from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def HOME_ROUTE():
    return {"response": [1,2,3,4,5]}


@app.route("/params/<one>/<two>", methods=["GET", "POST"])
def PARAMS_ROUTE(one, two):
    if (request.method) == "GET":
        return {
            "one": one,
            "two": two,
            "query": request.args.get("cheese")
        }
    if (request.method) == "POST":
        body = request.json
        return body