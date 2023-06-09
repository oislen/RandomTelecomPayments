import argparse


def commandline_interface():
    """A commandline interface for parsing input parameters with

    Windows
    python RandomTeleComData\scripts\main.py --factor 0.5 --randomseed 1 --nitr 3

    Linux
    python3 RandomTeleComData/scripts/main.py --factor 0.5 --randomseed 1 --nitr 3

    Parameters
    ----------

    Returns
    -------
    dict
        A dictionary of key, value pairs where the values are parsed input parameters
    """
    # define argument parser object
    parser = argparse.ArgumentParser(
        description="Execute Random TeleCom Data Programme."
    )
    # add input arguments
    parser.add_argument(
        "--factor",
        action="store",
        dest="factor",
        type=float,
        default=1,
        help="Float, multiplicative effect on number of users to generate",
    )
    parser.add_argument(
        "--randomseed",
        action="store",
        dest="randomseed",
        type=int,
        default=0,
        help="Integer, set a random seed for reproducible results; must be either 0 or 1",
    )
    parser.add_argument(
        "--nitr",
        action="store",
        dest="nitr",
        type=int,
        default=1,
        help="Integer, number of iterations to run",
    )
    # create an output dictionary to hold the results
    input_params_dict = {}
    # extract input arguments
    args = parser.parse_args()
    # map input arguments into output dictionary
    input_params_dict["factor"] = args.factor
    input_params_dict["randomseed"] = args.randomseed
    input_params_dict["nitr"] = args.nitr
    return input_params_dict
