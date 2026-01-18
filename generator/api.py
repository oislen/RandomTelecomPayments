import json
from fastapi import FastAPI

import cons
from main import main
from utilities.check_message_body import check_message_body
from utilities.JsonEncoder import JsonEncoder as NpEncoder

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to Random Telecom Payments API"}

@app.get("/api")
def get_api():
    output_data_dict = main(input_params_dict=cons.default_input_params_dict)
    trans_data_dict = output_data_dict['trans_data'].to_dict(orient='records')
    response = json.dumps(trans_data_dict, cls=NpEncoder)
    return response

@app.post("/api")
def post_api(body: dict):
    check_message_body(body)
    output_data_dict = main(input_params_dict=body)
    trans_data_dict = output_data_dict['trans_data'].to_dict(orient='records')
    response = json.dumps(trans_data_dict, cls=NpEncoder)
    return response