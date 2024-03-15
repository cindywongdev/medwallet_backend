from flask import Flask, request
import requests

app = Flask(__name__)

response = requests.get("https://randomuser.me/api")

@app.route("/", methods=["GET"])
def HOME_ROUTE():
    return {"response": "Welcome Home :)"}


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
    
@app.route("/randomuser", methods=["GET"])
def RANDOM_USER_ROUTE():
    return response.json()
    
@app.route("/gender", methods=["GET"])
def GENDER_ROUTE():
    gender = response.json()["results"][0]["gender"]
    return gender