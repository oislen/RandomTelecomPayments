# python generator/batch/gen_user_names_file.py

import os
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

system_prompt = """# Task

You are a name generator for people from different countries in Europe. Your task is to generate an arbitrary N number of distinct and varied first names and last names for people from a given European country of origin.

# Requirements

- Generate typical names for both male and female people.
- The names do not need to be traditional to the target European country.
- Do not repeat any first names or last names more than once. Each individual first name must be unique and each individual last name must be unique.
- You should return the first names and last names using a valid JSON object tagged as <answer></answer>.
- The valid JSON object should be of the following structure; {"firstnames":["first name 1","first name 2",...,"first name N"], "lastnames":["last name 1","last name 2",...,"last name N"]}

# Examples

- Generate 2 first names and 2 last names for people from the country "Germany" -> <answer>{"firstnames":["Max","Hannah"], "lastnames":["Müller","Schmidt"]}</answer>
- Generate 4 first names and 4 last names for people from the country "United Kingdom" -> <answer>{"firstnames":["George","Richard","Katie","Mary"], "lastnames":["Smith","Taylor","Jones","Brown"]}</answer>
- Generate 3 first names and 3 last names for people from the country "France" -> <answer>{"firstnames":["Lola","Mathieu","Léa"], "lastnames":["Benoît","Pierre","Lefort"]}</answer>
- Generate 5 first names and 5 last names for people from the country "Spain" -> <answer>{"firstnames":["Juan","Cristina","Javier","Julia","Isabel"], "lastnames":["Garcia","Martinez","Rodriguez","Lopez","Gomez"]}</answer>
- Generate 6 first names and 6 last names for people from the country "Sweden" -> <answer>{"firstnames":["Tova","Alva","Casper","Märta","Axel","Elsa"], "lastnames":["Andersson","Johansson","Lundberg","Svensson","Pettersson","Nilsson"]}</answer>
"""

prompt = 'Generate {n_user_names} first names and {n_user_names} last names for people from the country "{country}"'

bedrock_config = {
    "inferenceConfig":{
        "maxTokens":8192,
        "temperature":0.5,
        "topP":0.5,
    },
    "system":[
        {
            "text":system_prompt
        }
    ]
}

def invoke_bedrock(
    model:Bedrock,
    model_id:str,
    n_user_names:int,
    country:str,
    countrieseurope:pd.DataFrame,
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
    n_user_names : int
        The number of user names to generate.
    country : str
        The country for which to generate names.
    countrieseurope : pd.DataFrame
        A DataFrame containing country information for merging.
    
    Returns
    -------
    tuple:
        A tuple containing two pandas DataFrames:
            - tmp_firstname_country_data (pd.DataFrame): DataFrame with deduplicated and standardized first names along with country information.
            - tmp_lastname_country_data (pd.DataFrame): DataFrame with deduplicated and standardized last names along with country information.
    
    Raises
    ------
    json.JSONDecodeError: If the model response cannot be parsed as JSON.
    KeyError: If the expected keys ("firstnames", "lastnames") are missing from the JSON response.
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
    formatted_prompt = prompt.format(n_user_names=n_user_names, country=country)
    messages = [{"role":"user", "content":[{"text":formatted_prompt}]}]
    logging.info(messages)
    model_response = model.prompt(model_id=model_id, user_prompt=formatted_prompt, system_prompt=system_prompt, max_gen_len=2048)
    #model_response = model.converse(modelId=model_id, messages=messages, system=bedrock_config['system'], inference_config=bedrock_config['inferenceConfig'])
    # split out answer
    text = model_response.split("<answer>")[1].split("</answer>")[0]
    # parse json
    try:
        record_set = json.loads(text)
    except json.JSONDecodeError as e:
        raise Exception(f"Error parsing JSON: {e}")
    logging.info("Processing results ...")
    # generate pandas dataframe
    user_firstname_data = pd.Series(record_set["firstnames"], name="firstnames").to_frame().drop_duplicates(subset=["firstnames"])
    user_lastname_data = pd.Series(record_set["lastnames"], name="lastnames").to_frame().drop_duplicates(subset=["lastnames"])
    # add country
    user_firstname_data['country'] = country
    user_lastname_data['country'] = country
    # join on country codes
    llama_firstname_country_data = user_firstname_data.merge(right=countrieseurope, left_on='country', right_on='name', how='inner').drop(columns=['name'])
    llama_lastname_country_data = user_lastname_data.merge(right=countrieseurope, left_on='country', right_on='name', how='inner').drop(columns=['name'])
    # print shapes
    logging.info(f"llama_firstname_country_data.shape: {llama_firstname_country_data.shape}")
    logging.info(f"llama_lastname_country_data.shape: {llama_lastname_country_data.shape}")
    # format output file paths
    fpath_temp_llama_firstnames = cons.fpath_temp_llama_firstnames.format(country=country.lower())
    fpath_temp_llama_lastnames = cons.fpath_temp_llama_lastnames.format(country=country.lower())
    # check against previous iterations
    tmp_firstname_country_data = pd.DataFrame()
    tmp_lastname_country_data = pd.DataFrame()
    if os.path.exists(fpath_temp_llama_firstnames):
        tmp_firstname_country_data = pd.read_csv(fpath_temp_llama_firstnames, encoding="latin1")
    if os.path.exists(fpath_temp_llama_lastnames):
        tmp_lastname_country_data = pd.read_csv(fpath_temp_llama_lastnames, encoding="latin1")
    # concatenate results
    tmp_firstname_country_data = pd.concat(objs=[tmp_firstname_country_data, llama_firstname_country_data], axis=0, ignore_index=True)
    tmp_lastname_country_data = pd.concat(objs=[tmp_lastname_country_data, llama_lastname_country_data], axis=0, ignore_index=True)
    # standardise names formatting
    standardise_text_lambda = lambda x: unidecode.unidecode(" ".join(x.lower().strip().split())) if pd.isna(x) else x
    tmp_firstname_country_data["firstnames"] = tmp_firstname_country_data["firstnames"].apply(lambda x: standardise_text_lambda(x))
    tmp_lastname_country_data["lastnames"] = tmp_lastname_country_data["lastnames"].apply(lambda x: standardise_text_lambda(x))
    # deduplicate data
    tmp_firstname_country_data = tmp_firstname_country_data.drop_duplicates(subset=["firstnames"])
    tmp_lastname_country_data = tmp_lastname_country_data.drop_duplicates(subset=["lastnames"])
    # print shapes
    logging.info(f"tmp_firstname_country_data.shape: {tmp_firstname_country_data.shape}")
    logging.info(f"tmp_lastname_country_data.shape: {tmp_lastname_country_data.shape}")
    # save firstnames names data to temp directory (if pairwise firstnames have been created)
    if tmp_firstname_country_data.shape[0] >= llama_firstname_country_data.shape[0]:
        tmp_firstname_country_data.to_csv(fpath_temp_llama_firstnames, index=False, encoding="latin1")
        logging.info(f"Wrote {fpath_temp_llama_firstnames} ...")
    # save lastnames data to temp directory (if pairwise lastnames have been created)
    if tmp_lastname_country_data.shape[0] >= llama_lastname_country_data.shape[0]:
        tmp_lastname_country_data.to_csv(fpath_temp_llama_lastnames, index=False, encoding="latin1")
        logging.info(f"Wrote {fpath_temp_llama_lastnames} ...")
    return (tmp_firstname_country_data, tmp_lastname_country_data)

def main(bedrock, model_id, run_bedrock=False):
    """
    Docstring for main
    """
    
    # load countries, firstnames and surnames files
    countrieseurope = pd.read_csv(cons.fpath_countries_europe, usecols=['name', 'ISO numeric'])
    orig_firstnames = pd.read_csv(cons.fpath_firstnames)
    orig_surnames = pd.read_csv(cons.fpath_lastnames)
    # determine file size
    orig_filesize = int((orig_firstnames.shape[0] + orig_surnames.shape[0])/2)
    n_countries = countrieseurope.shape[0]
    n_user_names = min(2, int(orig_filesize / n_countries))
    # generate user names
    firstname_country_data, lastname_country_data, error_countries = [], [], []
    # set countries list
    #countries_list = countrieseurope['name'].to_list()
    countries_list = ['Cyprus']
    
    # iterate over countries list
    for country in countries_list:
        logging.info(f"{country} ...")
        try:
            if run_bedrock:
                # call bedrock model and generate user names data
                tmp_firstname_country_data, tmp_lastname_country_data = invoke_bedrock(model=bedrock, model_id=model_id, n_user_names=n_user_names, country=country, countrieseurope=countrieseurope)
                logging.info("Waiting ...")
                # wait 20 seconds before retrying
                time.sleep(20)
            else:
                tmp_firstname_country_data = pd.read_csv(cons.fpath_temp_llama_firstnames.format(country=country.lower()), encoding="latin1")
                tmp_lastname_country_data = pd.read_csv(cons.fpath_temp_llama_lastnames.format(country=country.lower()), encoding="latin1")
            # append to user country data
            firstname_country_data.append(tmp_firstname_country_data)
            lastname_country_data.append(tmp_lastname_country_data)
        except Exception as e:
            logging.info(e)
            error_countries.append(country)
    
    # log if any countries failed to generate data
    if len(error_countries) > 0:
        logging.info(f"Failed to generated data for countries: {error_countries}")
    
    # load existing reference data
    firstname_country_df = pd.read_csv(cons.fpath_llama_firstnames, encoding="latin1")
    lastname_country_df = pd.read_csv(cons.fpath_llama_lastnames, encoding="latin1")
    # append to country data lists
    firstname_country_data.append(firstname_country_df)
    lastname_country_data.append(lastname_country_df)
    # concatenate user country data together and deduplicate across firstnames and countries
    output_firstname_country_df = pd.concat(firstname_country_data, axis=0, ignore_index=True)
    output_lastname_country_df = pd.concat(lastname_country_data, axis=0, ignore_index=True)
    # sort and deduplicate output data
    output_firstname_country_df = output_firstname_country_df.drop_duplicates(subset=["country","firstnames"]).sort_values(by=["country","firstnames"])
    output_lastname_country_df = output_lastname_country_df.drop_duplicates(subset=["country","lastnames"]).sort_values(by=["country","lastnames"])
    
    # write data to disk
    if output_firstname_country_df['country'].nunique() == n_countries:
        logging.info(f"output_firstname_country_df.shape: {output_firstname_country_df.shape}")
        output_firstname_country_df.to_csv(cons.fpath_llama_firstnames, index=False, encoding="latin1")
    else:
        logging.info("WARNING Insufficient first name data generated.")
    if output_lastname_country_df['country'].nunique() == n_countries:
        logging.info(f"output_lastname_country_df.shape: {output_lastname_country_df.shape}")
        output_lastname_country_df.to_csv(cons.fpath_llama_lastnames, index=False, encoding="latin1")
    else:
        logging.info("WARNING Insufficient last name data generated.")

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
    main(bedrock=bedrock, run_bedrock=True, model_id=model_id)

