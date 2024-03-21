from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# ------------------------------------------------------------------------------------
# write function here to dynamically return API endpoint w/ most recent year's data
# ------------------------------------------------------------------------------------

# but for now, just use static endpoint for 2022 general payments
response = requests.get("https://openpaymentsdata.cms.gov/api/1/datastore/query/66dfcf9a-2a9e-54b7-a0fe-cae3e42f3e8f")

@app.route("/", methods=["GET"])
def HOME_ROUTE():
    return {"response": "Welcome Home :)"}
    
@app.route("/data", methods=["GET", "POST"])
def DATA_ROUTE():  
    if (request.method) == "POST":
        currentPage = request.json["currentPage"]
        print(currentPage)
        offset = (currentPage - 1) * 50
        
        single_page_response = requests.get(f"https://openpaymentsdata.cms.gov/api/1/datastore/query/66dfcf9a-2a9e-54b7-a0fe-cae3e42f3e8f?limit=50&offset={offset}")
        
        
    # all_payments = response.json()["results"]
    all_payments = single_page_response.json()["results"]
    
    # The following code returns all payments > $10. This is because all the fields in database are string types. Although the API offers using SQL in the endpoints as an option to return a specific query, it doesn't work when interacting with non-string types, such as floats, in this case. Therefore it must be manually done in this backend.
    payments_over_10 = []
    for payment in all_payments: 
        payment_int = float(payment["total_amount_of_payment_usdollars"])
        payments_over_10.append(payment) if payment_int >= 10 else None
    
    return payments_over_10
    
# @app.route("/params/<one>/<two>", methods=["GET", "POST"])
# def PARAMS_ROUTE(one, two):
#     if (request.method) == "GET":
#         return {
#             "one": one,
#             "two": two,
#             "query": request.args.get("cheese")
#         }
#     if (request.method) == "POST":
#         body = request.json #do i need () here for request?
#         return body