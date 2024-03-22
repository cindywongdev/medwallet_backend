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
    search_url=f'https://openpaymentsdata.cms.gov/api/1/datastore/sql?query=[SELECT * FROM 66dfcf9a-2a9e-54b7-a0fe-cae3e42f3e8f][WHERE covered_recipient_primary_type_1 = "{recipient_type}"][LIMIT 50]'
    response = requests.get(search_url)
    search_results = response.json()
    
    # For this API endpoint, the response consists of objects with title-case keys, which is different from the endpoint in the DATA_ROUTE, which returns lowercase keys. As such, the frontend has been written to access lowercase keys and cannot access these title-case keys. Therefore, the following code converts all the keys to lowercase.
    search_results_lowercase = []
    for search_result in search_results:
        search_result_lowercase = {}
        for key, value in search_result.items():
            search_result_lowercase[key.lower()] = value
        search_results_lowercase.append(search_result_lowercase)
    return search_results_lowercase
    # On Efficiency: While the above code has a high Time Complexity of 0(n^2), I chose to handle this issue on the backend rather than manipulating the frontend because:
        # 1) It follows the logic of the DATA_ROUTE above where the data is manipulated to a satisfactory quality, such that the frontend can consume it without more manipulation.
        # 2) The frontend code becomes messy when written to accept both cases.
        # 3) The size of the response is limited to 50, which is currently manageable. If that were to increase significantly, it may be better to manipulate the frontend to accept both cases.