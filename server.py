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
    
@app.route("/data/<currentPage>", methods=["GET", "POST"])
def DATA_ROUTE(currentPage):
    # Offset refers to the number of records to skip before querying the # of records specified by the limit parameter. This is useful for making smaller API calls based on the page number sent by the frontend, which is what is being done here.
    offset = (int(currentPage) - 1) * 50
    data_url = f"https://openpaymentsdata.cms.gov/api/1/datastore/query/66dfcf9a-2a9e-54b7-a0fe-cae3e42f3e8f?limit=50&offset={offset}"
    single_page_response = requests.get(data_url)
    all_payments = single_page_response.json()["results"]
    
    # The following code manipulates the response to only payments > $10. This is because all the fields in database are string types. Although the API offers using SQL in the endpoints as an option to return a specific query, it doesn't work when interacting with non-string types, such as floats, in this case. Therefore it must be manually done in this backend.
    payments_over_10 = []
    for payment in all_payments: 
        payment_int = float(payment["total_amount_of_payment_usdollars"])
        payments_over_10.append(payment) if payment_int >= 10 else None
    
    return payments_over_10

@app.route("/search/<recipient_type>", methods=["GET"])
def SEARCH_ROUTE(recipient_type):
    search_url=f'https://openpaymentsdata.cms.gov/api/1/datastore/sql?query=[SELECT * FROM 66dfcf9a-2a9e-54b7-a0fe-cae3e42f3e8f][WHERE covered_recipient_primary_type_1 = "{recipient_type}"][LIMIT 1]'
    response = requests.get(search_url)
    search_results = response.json()
    
    return search_results