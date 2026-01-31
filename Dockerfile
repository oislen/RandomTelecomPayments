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
RUN apt-get install -y imagemagick=8:7.1.1.43+dfsg1-1+deb13u5 libssl-dev=3.5.4-1~deb13u2

# set up home environment
RUN adduser ${user}
RUN mkdir -p /home/${user} && chown -R ${user}: /home/${user}

# copy repo
COPY . /home/${user}/RandomTelecomPayments

# set working directory for random telecom payments app
WORKDIR /home/${user}/RandomTelecomPayments

# install required python packages
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN uv sync

EXPOSE 8000
ENTRYPOINT  ["uv", "run", "generator/main.py"]