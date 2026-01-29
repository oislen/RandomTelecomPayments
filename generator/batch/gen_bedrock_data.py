# python generator/batch/gen_bedrock_data.py

import json
import boto3
from botocore.config import Config
import sys
import time
import logging
import unidecode
import pandas as pd
import numpy as np

sys.path.append("E:\\GitHub\\RandomTelecomPayments\\generator")

import cons
from utilities.Bedrock import Bedrock

system_name_prompt = """# Task

You are a name generator for people from different countries in Europe.
Your task is to generate an arbitrary N number of distinct and varied first names, or last names, for people from a given European country of origin.

# Requirements

- Generate typical names for both male and female people.
- The names do not need to be traditional to the target European country.
- Do not repeat any first names or last names more than once.
- Each individual first name must be unique and each individual last name must be unique.
- You should return the first names and last names using a valid JSON object tagged as <answer></answer>.
- The valid JSON object should be of the following structures; `["name 1","name 2",...,"name N"]`.

# Examples

## First Names

- Generate 2 first names for people from the country "Germany" -> <answer>["Max","Hannah"]</answer>
- Generate 4 first names for people from the country "United Kingdom" -> <answer>["George","Richard","Katie","Mary"]</answer>
- Generate 3 first names for people from the country "France" -> <answer>["Lola","Mathieu","Léa"]</answer>
- Generate 5 first names for people from the country "Spain" -> <answer>["Juan","Cristina","Javier","Julia","Isabel"]</answer>
- Generate 6 first names for people from the country "Sweden" -> <answer>["Tova","Alva","Casper","Märta","Axel","Elsa"]</answer>

## Last Names

- Generate 2 last names for people from the country "Germany" -> <answer>["Müller","Schmidt"]</answer>
- Generate 4 last names for people from the country "United Kingdom" -> <answer>["Smith","Taylor","Jones","Brown"]</answer>
- Generate 3 last names for people from the country "France" -> <answer>["Benoît","Pierre","Lefort"]</answer>
- Generate 5 last names for people from the country "Spain" -> <answer>["Garcia","Martinez","Rodriguez","Lopez","Gomez"]</answer>
- Generate 6 last names for people from the country "Sweden" -> <answer>["Andersson","Johansson","Lundberg","Svensson","Pettersson","Nilsson"]</answer>
"""

system_email_prompt = """
"""

first_name_prompt = 'Generate {n_data_points} first names for people from the country "{country}"'
surname_prompt = 'Generate {n_data_points} last names for people from the country "{country}"'
email_domain_prompt = 'Generate {n_data_points} popular email domains names for people from the country "{country}"'

bedrock_config = {
    "inferenceConfig":{
        "maxTokens":8192,
        "temperature":0.5,
        "topP":0.5,
    },
    "system":[
        {
            "text":system_name_prompt
        }
    ]
}

def invoke_bedrock(
    model:Bedrock,
    model_id:str,
    data_point:str,
    n_data_points:int,
    country:str,
    countrieseurope:pd.DataFrame,
    prompt:str,
    system_prompt:str,
    country_fpath:str,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Invokes the Bedrock model to generate user names for a specified country.
    
    This function calls the Bedrock model with a formatted prompt to generate first names
    and last names for a given country. It processes the model's response, parses the JSON
    output, and merges the results with country data. The function deduplicates and standardizes
    the name formatting, then persists the data to temporary CSV files.
    
    Parameters
    ----------
    model : Bedrock
        The Bedrock model instance used to generate names.
    n_data_points : int
        The number of data points to generate
    country : str
        The country for which to generate names.
    countrieseurope : pd.DataFrame
        A DataFrame containing country information for merging.
    
    Returns
    -------
    tuple:
        A tuple containing two pandas DataFrames:
            - tmp_first_name_country_data (pd.DataFrame): DataFrame with deduplicated and standardized first names along with country information.
            - tmp_last_name_country_data (pd.DataFrame): DataFrame with deduplicated and standardized last names along with country information.
    
    Raises
    ------
    json.JSONDecodeError: If the model response cannot be parsed as JSON.
    KeyError: If the expected keys ("first_names", "last_names") are missing from the JSON response.
    Exception: If the merge with country data fails or file I/O operations encounter errors.
    
    Notes
    -----
    - Names are standardized by converting to lowercase, removing extra whitespace, and applying Unicode normalization using unidecode.
    - Duplicate names are removed after each processing step.
    - Results are concatenated with any previously generated data for the same country and saved to temporary CSV files if the new data increases the dataset size.
    - CSV files are encoded in latin1 format.
    
    """
    logging.info("Calling Bedrock ...")
    # call bedrock model
    formatted_prompt = prompt.format(n_data_points=n_data_points, country=country)
    messages = [{"role":"user", "content":[{"text":formatted_prompt}]}]
    logging.info(messages)
    #model_response = model.prompt(model_id=model_id, user_prompt=formatted_prompt, system_prompt=system_prompt, max_gen_len=2048)
    model_response = model.converse(modelId=model_id, messages=messages, system=bedrock_config['system'], inference_config=bedrock_config['inferenceConfig'])
    # split out answer
    text = model_response.split("<answer>")[1].split("</answer>")[0]
    # parse json
    try:
        gen_data_list = json.loads(text)
    except json.JSONDecodeError as e:
        raise Exception(f"Error parsing JSON: {e}")
    logging.info("Processing results ...")
    # generate pandas dataframe
    gen_dataframe = pd.Series(gen_data_list, name=data_point).drop_duplicates().to_frame()
    gen_dataframe['country'] = country
    gen_country_dataframe = pd.merge(
        left=gen_dataframe,
        right=countrieseurope.rename(columns={'name':'country'}),
        left_on='country',
        right_on='name',
        how='inner'
        )
    # standardise names formatting
    standardise_text_lambda = lambda x: unidecode.unidecode(" ".join(x.strip())) if pd.isna(x) else x
    gen_country_dataframe[data_point] = gen_country_dataframe[data_point].apply(lambda x: standardise_text_lambda(x))
    logging.info(f"gen_country_dataframe.shape: {gen_country_dataframe.shape}")
    # save generated data
    gen_country_dataframe.to_csv(country_fpath, index=False, encoding="latin1")
    logging.info(f"Wrote {country_fpath} ...")
    return gen_country_dataframe

def main(bedrock, model_id, data_point, fpath_dict, run_bedrock=False):
    """
    Docstring for main
    """
    # load countries, first_names and surnames files
    countrieseurope = pd.read_csv(cons.fpath_countries_europe, usecols=['name', 'ISO numeric'])
    n_countries = countrieseurope.shape[0]
    # set lists to collect generated data with
    gen_country_dataframe_list, error_countries = [], []
    # set countries list
    #countries_list = countrieseurope['name'].to_list()
    countries_list = ['Cyprus']
    # iterate over countries list
    for country in countries_list:
        logging.info(f"{country} ...")
        country_fpath=fpath_dict['country_fpath'].format(country)
        try:
            if run_bedrock:
                # call bedrock model and generate user names data
                country_filter = (countrieseurope["name"] == country)
                country_population = countrieseurope.loc[country_filter, "population"].iloc[0]
                # set n data points for ai generator depending on type
                if data_point in ("first_names", "last_names"):
                    n_data_points = int(np.log(country_population)**1.5)
                elif data_point == "email_domains":
                    n_data_points = 5
                else:
                    raise ValueError(f"Invalid parameter data_point value {data_point}")
                # invoke bedrock and generate data points
                tmp_gen_country_data = invoke_bedrock(
                    model=bedrock,
                    model_id=model_id,
                    data_point=data_point,
                    n_data_points=n_data_points,
                    country=country,
                    countrieseurope=countrieseurope,
                    country_fpath=country_fpath
                    )
                logging.info("Waiting ...")
                # wait 20 seconds before retrying
                time.sleep(20)
            else:
                tmp_gen_country_data = pd.read_csv(country_fpath, encoding="latin1")
            # append to user country data
            gen_country_dataframe_list.append(tmp_gen_country_data)
        except Exception as e:
            logging.info(e)
            error_countries.append(country)
    # log if any countries failed to generate data
    if len(error_countries) > 0:
        logging.info(f"Failed to generated data for countries: {error_countries}")
    # concatenate user country data together and deduplicate across first_names and countries
    output_gen_country_dataframe = pd.concat(gen_country_dataframe_list, axis=0, ignore_index=True)
    # sort and deduplicate output data
    sort_dedup_cols = ["country",data_point]
    output_gen_country_dataframe = output_gen_country_dataframe.drop_duplicates(subset=sort_dedup_cols).sort_values(by=sort_dedup_cols)
    # write data to disk
    if output_gen_country_dataframe['country'].nunique() == n_countries:
        logging.info(f"output_gen_country_dataframe.shape: {output_gen_country_dataframe.shape}")
        output_gen_country_dataframe.to_csv(fpath_dict["fpath"], index=False, encoding="latin1")
    else:
        logging.info("WARNING Insufficient first name data generated.")

lgr = logging.getLogger()
lgr.setLevel(logging.INFO)

if __name__ == "__main__":
    # set aws region
    aws_region = "us-east-1"
    model_id="us.meta.llama3-1-70b-instruct-v1:0"
    # load aws config
    with open(cons.fpath_aws_session_token, "r") as j:
        aws_config = json.loads(j.read())
    # connect to aws boto3
    session = boto3.Session(
        aws_access_key_id=aws_config['Credentials']["AccessKeyId"],
        aws_secret_access_key=aws_config['Credentials']["SecretAccessKey"],
        aws_session_token=aws_config['Credentials']["SessionToken"],
        region_name=aws_region
    )
    bedrock_runtime = session.client(
        service_name="bedrock-runtime",
        region_name=aws_region,
        config=Config(retries={"max_attempts":1, "mode": "adaptive"})
        )
    # create bedrock instance
    bedrock = Bedrock(bedrock_runtime=bedrock_runtime)
    # execute main programme
    for data_point, fpath_dict in cons.llama_data_point_fpaths.items():
        main(bedrock=bedrock, model_id=model_id, data_point=data_point, fpath_dict=fpath_dict, run_bedrock=True)

