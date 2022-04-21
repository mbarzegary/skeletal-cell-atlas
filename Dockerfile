# set base image (host OS)
FROM python:3.8-slim as base

# Build layer
FROM base as build

# Install depedencies for build
RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean

RUN pip install --upgrade pip

WORKDIR /app
COPY requirements.txt requirements.txt

# install dependencies
RUN pip install -r requirements.txt --prefix=/install

# Build production image
FROM base
# Default port to serve the app
ENV SERVER_PORT 8050

# Default data path
ENV DATA_PATH /app/data

# set the working directory in the container
WORKDIR /app

RUN mkdir -m 777 /app/cache 
ENV NUMBA_CACHE_DIR /app/cache
RUN mkdir -m 777 /app/data

# copy build dependencies
COPY --from=build /install /usr/local

COPY entrypoint.sh .
COPY files files
COPY app app

# command to run on container start
ENTRYPOINT ["/app/entrypoint.sh"]
