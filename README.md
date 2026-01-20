# Random Telecom Payments Generation

## Overview

Randomly simulated data is particularly useful when it's real world counterpart is hard access due to complexity, privacy and security reasons. Moreover, randomly simulated data has additional benefits including reproducibility, scalability and controllability.

This application aims to simulate telecommunication payments using random number generation. It includes typical transaction level relationships and behaviours amongst the user, device, ip, and card entities. It can be used in place of real world telecommunication payments for prototyping solutions and as an education tool.

The data generation algorithm works by first generating user level telecom payments data. Afterwards, the user level data is exploded to transaction level, and any inconsistencies within the data model are removed. Finally, the transaction status and error codes are generated using underlying features within the transaction level data.

### Master File

A stable master version of the Random Telecom Payments data can be found on Kaggle here:

* https://www.kaggle.com/datasets/oislen/randomtelecompayments

## Data Model

The underlying data model present in the simulated telecommunication payments is displayed below.

![Entity Relationship Diagram](doc/entity_relationship_diagram.jpg)

For a more detailed account of each column in the dataset see the data dictionary:

* https://github.com/oislen/RandomTelecomPayments/blob/main/doc/data_dictionary.csv

## Running the Application (Windows)

### Anaconda

Create a local conda environment for the Random Telecom Payments app using [anaconda](https://www.anaconda.com/):

```
conda create --name RandomTelecomPayments python=3.12 --yes
conda activate RandomTelecomPayments
pip install -r requirements.txt
```

Execute the Random Telecom Payments app to generate data for 2000 users using the following command and the local conda environment:

```
python generator\\main.py --n_users 1000 --use_random_seed 1 --n_itr 2
```

View the generated Random Telecom Payments data using the following command:

```
type data\\RandomTelecomPayments.csv | more
```

### Docker

The latest version of the Random Telecom Payments app can be found as a [docker](https://www.docker.com/) image on dockerhub here:

* https://hub.docker.com/repository/docker/oislen/randomtelecompayments/general

The docker image can be pulled from dockerhub using the following command:

```
docker pull oislen/randomtelecompayments:latest
```

The Random Telecom Payments app can then be executed to generate data for 2000 users using the following command and the docker image:

```
docker run --name rtp oislen/randomtelecompayments:latest --n_users 1000 --use_random_seed 1 --n_itr 2
```

The generated Random Telecom Payments data can then be extract from the docker image using the following command:

```
docker cp rtp:/home/user/RandomTelecomPayments/data/RandomTelecomPayments.csv %userprofile%\Downloads\RandomTelecomPayments.csv
```

### Application Parameters

* **n_users** - integer, the number of users to generate Random Telecom Payments data for, default is 100.
* **use_random_seed** - integer, whether to run the Random Telecom Payments data generation with or without a random seed set for reproducible results; must be 0 or 1.
* **n_itr** - integer, the number of Random Telecom Payments data batches to generate; must be at least 1. The python multiprocessing library is used to run each in parallel across all available cores.
* **registration_start_date** - string, the start date for user registrations, default is two years ago from today.
* **registration_end_date** - string, the end date for user registrations, default is one year ago from today.
* **transaction_start_date** - string, the start date for user transactions, default is one year ago from today.
* **transaction_end_date** - string, the end date for user transactions, default is today.
