from beartype import beartype
from typing import Dict

@beartype
def input_error_handling(
    input_params_dict:Dict[str, object],
    ):
    """
    Runs error handling on the input params dictionary.
    
    Parameters
    ----------
    input_params_dict : Dict[str, object]
        A dictionary of input parameters.
    
    Examples
    --------
    ```
    input_params_dict = {'n_users': 1000, 'use_random_seed': 1, 'n_itr': 10}
    input_error_handling(input_params_dict=input_params_dict)
    ```
    """
    # check if the n users parameter is positive
    if not ((input_params_dict["n_users"] >= 1) and (isinstance(input_params_dict["n_users"], int))):
        raise ValueError(f"Invalid n_users parameter value {input_params_dict['n_users']}; must be a integer >= 1.")
    # check if the random seed is either 0 or 1
    if not ((input_params_dict["use_random_seed"] in (0, 1)) and (isinstance(input_params_dict["use_random_seed"], int))):
        raise ValueError(f"Invalid use_random_seed value {input_params_dict['use_random_seed']}; must be either 0 or 1.")
    # check if the number of iterations is greater than or equal to 1
    if not ((input_params_dict["n_itr"] >= 1) and (isinstance(input_params_dict["n_itr"], int))):
        raise ValueError(f"Invalid n_itr parameter value {input_params_dict['n_itr']}; must be an integer >= 1.")
    # check if the number of applications is positive
    if not ((input_params_dict["n_applications"] >= 1) and (isinstance(input_params_dict["n_applications"], int))):
        raise ValueError(f"Invalid n_applications parameter value {input_params_dict['n_applications']}; must be a integer >= 1.")
