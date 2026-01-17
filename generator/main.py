import os
import sys
import logging
from time import time
import pandas as pd

sys.path.append(os.path.join(os.getcwd(), 'generator'))

import cons
from utilities.commandline_interface import commandline_interface
from utilities.input_error_handling import input_error_handling
from utilities.multiprocess import multiprocess
from app.gen_random_telecom_data import gen_random_telecom_data

if __name__ == '__main__':

    # set up logging
    lgr = logging.getLogger()
    lgr.setLevel(logging.INFO)

    # set user parameters
    input_params_dict = commandline_interface()

    # run input error handling
    input_error_handling(input_params_dict)

    logging.info(f'Input Parameters: {input_params_dict}')

    # start timer
    t0 = time()
    if input_params_dict['n_itr'] > 1:
        logging.info("Running multi-thread.")
        # generate random telecom data via multiprocess call
        args = [
            (
                input_params_dict['n_users'],
                None if input_params_dict['use_random_seed'] == 0 else itr,
                input_params_dict['n_applications'],
                input_params_dict['registration_start_date'],
                input_params_dict['registration_end_date'],
                input_params_dict['transaction_start_date'],
                input_params_dict['transaction_end_date']
            ) for itr in range(input_params_dict['n_itr'])
            ]
        results = multiprocess(func = gen_random_telecom_data, args = args, ncpu = os.cpu_count())
    else:
        logging.info("Running single thread.")
        results = [
            gen_random_telecom_data(
                n_users=input_params_dict['n_users'],
                random_seed=input_params_dict['use_random_seed'],
                n_applications=input_params_dict['n_applications'],
                registration_start_date=input_params_dict['registration_start_date'],
                registration_end_date=input_params_dict['registration_end_date'],
                transaction_start_date=input_params_dict['transaction_start_date'],
                transaction_end_date=input_params_dict['transaction_end_date']
                )
            ]
    # concatenate random telecom datasets into a single file
    user_data = pd.concat(objs = [result['user_data'] for result in results], axis = 0, ignore_index = True)
    trans_data = pd.concat(objs = [result['trans_data'] for result in results], axis = 0, ignore_index = True)
    # TODO: add addition post processing if running multi-processing due to random duplicates between iterations
    # order results by userid and transaction date ascending
    user_data = user_data.sort_values(by = 'uid').reset_index(drop = True)
    trans_data = trans_data.sort_values(by = 'transaction_date').reset_index(drop = True)
    # end timer
    t1 = time()
    total_runtime_seconds = round(t1 - t0, 2)
    logging.info(f'Total Runtime: {total_runtime_seconds} seconds')

    # print out head and shape of data
    logging.info(f'RandomTeleComUsersData.shape: {user_data.shape}')
    logging.info(f'RandomTeleComTransData.shape: {trans_data.shape}')

    # check output data directories exist
    data_fdirs = [os.path.dirname(cons.fpath_randomtelecomtransdata), os.path.dirname(cons.fpath_randomtelecomusersdata)] 
    for data_fdir in data_fdirs:
        if not os.path.exists(data_fdir):
            os.mkdir(data_fdir)

    # write data to disk
    logging.info(f'Writing intermediate user level random telecoms data to: {cons.fpath_randomtelecomusersdata}')
    logging.info(f'Writing output trans level random telecoms data to: {cons.fpath_randomtelecomtransdata}')
    user_data.to_parquet(cons.fpath_randomtelecomusersdata, engine='fastparquet')
    trans_data.to_csv(cons.fpath_randomtelecomtransdata, index = False)