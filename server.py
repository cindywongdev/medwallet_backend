from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# write function here to dynamically return API endpoint w/ most recent year's data

# for now, just use static endpoint for 2022 general payments
response = requests.get("https://openpaymentsdata.cms.gov/api/1/datastore/query/66dfcf9a-2a9e-54b7-a0fe-cae3e42f3e8f")

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