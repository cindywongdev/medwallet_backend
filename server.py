from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# response = requests.get("https://randomuser.me/api")
response = requests.get("https://openpaymentsdata.cms.gov/api/1/metastore/schemas/dataset/items/df01c2f8-dc1f-4e79-96cb-8208beaf143c")

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
    
@app.route("/data", methods=["GET"])
def DATA_ROUTE():
    return response.json()
    
# @app.route("/randomuser", methods=["GET"])
# def RANDOM_USER_ROUTE():
#     return response.json()
    
# @app.route("/gender", methods=["GET"])
# def GENDER_ROUTE():
#     gender = response.json()["results"][0]["gender"]
#     return gender