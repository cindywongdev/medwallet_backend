from flask import Flask, request
import requests

app = Flask(__name__)

response = requests.get("https://randomuser.me/api")
print(f'hi {response.status_code}')

@app.route("/", methods=["GET"])
def HOME_ROUTE():
    return response.json()
    # return {"response": [1,2,3,4,5]}


@app.route("/params/<one>/<two>", methods=["GET", "POST"])
def PARAMS_ROUTE(one, two):
    if (request.method) == "GET":
        return {
            "one": one,
            "two": two,
            "query": request.args.get("cheese")
        }
    if (request.method) == "POST":
        body = request.json #do i need () here?
        return body