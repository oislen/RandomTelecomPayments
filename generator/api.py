import json
from fastapi import FastAPI, Query
from typing import Annotated, Dict, List

import cons
from main import main
from utilities.JsonEncoder import JsonEncoder as JsonEncoder

tags_metadata = [
    {
        "name": "Random Telecom Payments Data Generator",
        "description": "Generate random telecom payments data based on user-defined parameters.",
    },
]

app = FastAPI(
    title="Random Telecom Payments Data Generator API",
    description="An API to generate random telecom payments data based on user-defined parameters.",
    version="0.0.0",
    openapi_tags=tags_metadata,
)

@app.get("/api")
async def get_api(
    n_users: Annotated[int, Query(title="Number of Users", description="The number of users")] = cons.default_n_users,
    use_random_seed : Annotated[int, Query(title="Use Random Seed", description="The random seed to use", ge=0, le=1)] = cons.default_use_random_seed,
    n_itr : Annotated[int, Query(title="Number of Iterations", description="The number of iterations", ge=1)] = cons.default_n_itr,
    n_applications : Annotated[int, Query(title="Number of Applications", description="The number of applications", ge=1)] = cons.default_n_applications,
    registration_start_date : Annotated[str, Query(title="Registration Start Date", description="The registration start date in YYYY-MM-DD format")] = cons.default_registration_start_date,
    registration_end_date : Annotated[str, Query(title="Registration End Date", description="The registration end date in YYYY-MM-DD format")] = cons.default_registration_end_date,
    transaction_start_date : Annotated[str, Query(title="Transaction Start Date", description="The transaction start date in YYYY-MM-DD format")] = cons.default_transaction_start_date,
    transaction_end_date : Annotated[str, Query(title="Transaction End Date", description="The transaction end date in YYYY-MM-DD format")] = cons.default_transaction_end_date,
    #tags: list[str] = ["Random Telecom Payments Data Generator"]
    ):
    """
    Generate random telecom payments data based on user-defined parameters.
    
    Parameters
    ----------
    n_users : int
        The number of users.
    use_random_seed : int
        The random seed to use (0 or 1).
    n_itr : int
        The number of iterations.
    n_applications : int
        The number of applications.
    registration_start_date : str
        The registration start date in YYYY-MM-DD format.
    registration_end_date : str
        The registration end date in YYYY-MM-DD format.
    transaction_start_date : str
        The transaction start date in YYYY-MM-DD format.
    transaction_end_date : str
        The transaction end date in YYYY-MM-DD format.
    
    Returns
    -------
    response : str
        A JSON string containing the generated telecom payments data.
    """
    # generate parameters dictionary
    input_params_dict={
        "n_users": n_users,
        "use_random_seed": use_random_seed,
        "n_itr": n_itr,
        "n_applications": n_applications,
        "registration_start_date": registration_start_date,
        "registration_end_date": registration_end_date,
        "transaction_start_date": transaction_start_date,
        "transaction_end_date": transaction_end_date
    }
    # run random telecom payments generator
    output_data_dict = main(input_params_dict=input_params_dict)
    # convert transaction data to dictionary and then to json response
    trans_data_dict = output_data_dict['trans_data'].to_dict(orient='records')
    response = json.dumps(trans_data_dict, cls=JsonEncoder)
    return response

@app.post("/api")
async def post_api(
    body: Dict[str, object] = {},
    #tags: list[str] = ["Random Telecom Payments Data Generator"]
    ):
    """
    Generate random telecom payments data based on user-defined parameters.
    
    Parameters
    ----------
    body : Dict[str, object]
        A dictionary containing the input parameters.
        Possible keys are:
            - n_users : int
                The number of users.
            - use_random_seed : int
                The random seed to use (0 or 1).
            - n_itr : int
                The number of iterations.
            - n_applications : int
                The number of applications.
            - registration_start_date : str
                The registration start date in YYYY-MM-DD format.
            - registration_end_date : str
                The registration end date in YYYY-MM-DD format.
            - transaction_start_date : str
                The transaction start date in YYYY-MM-DD format.
            - transaction_end_date : str
                The transaction end date in YYYY-MM-DD format.
    
    Returns
    -------
    response : str
        A JSON string containing the generated telecom payments data.
    """
    # generate parameters dictionary
    input_params_dict={**cons.default_input_params_dict, **body}
    # run random telecom payments generator
    output_data_dict = main(input_params_dict=input_params_dict)
    # convert transaction data to dictionary and then to json response
    trans_data_dict = output_data_dict['trans_data'].to_dict(orient='records')
    response = json.dumps(trans_data_dict, cls=JsonEncoder)
    return response