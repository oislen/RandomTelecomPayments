# get base image
FROM python:3.12

# set environment variables
ENV user=user
ENV DEBIAN_FRONTEND=noninteractive
# set python version
ARG PYTHON_VERSION="3.12"
ENV PYTHON_VERSION=${PYTHON_VERSION}

# install required software and programmes for development environment
RUN apt-get update
RUN apt-get install -y apt-utils vim curl wget unzip tree htop adduser

# set up home environment
RUN adduser ${user}
RUN mkdir -p /home/${user} && chown -R ${user}: /home/${user}

# copy repo
COPY . /home/${user}/RandomTelecomPayments

# install required python packages
RUN python -m pip install -v -r /home/${user}/RandomTelecomPayments/requirements.txt

# set working directory for random telecom payments app
WORKDIR /home/${user}/RandomTelecomPayments

ENTRYPOINT  ["python", "generator/main.py"]