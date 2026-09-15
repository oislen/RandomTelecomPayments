# get base image
FROM python:3.12-slim@sha256:2fe5997d249a808b8eeea52c58a1dbffbba28754dc11699ef5c029f2d818ce79

# set environment variables
ENV user=user
ENV DEBIAN_FRONTEND=noninteractive
# set python version
ARG PYTHON_VERSION="3.12"
ENV PYTHON_VERSION=${PYTHON_VERSION}

# install required software and programmes for development environment
RUN apt-get update
RUN apt-get install -y apt-utils vim curl wget unzip tree htop adduser
# install trivy image vulnerability patches
RUN apt-get install -y gzip=1.13-1+deb13u1
RUN apt-get install -y libpcre2-8-0=10.46-1~deb13u2
RUN apt-get install -y libsqlite3-0=3.46.1-7+deb13u2
RUN apt-get install -y perl-base=5.40.1-6+deb13u1

# set up home environment
RUN adduser ${user}
RUN mkdir -p /home/${user} && chown -R ${user}: /home/${user}

# copy repo
COPY . /home/${user}/RandomTelecomPayments

# set working directory for random telecom payments app
WORKDIR /home/${user}/RandomTelecomPayments

# install required python packages
COPY --from=ghcr.io/astral-sh/uv@sha256:68224c7eb575bc13e4723f8831331db68555125fac3939fdde78cdb6000667ad /uv /uvx /bin/
RUN uv sync

EXPOSE 8000
ENTRYPOINT  ["uv", "run", "generator/main.py"]