# Skeletal Cell Atlas

## About

This repository contains the source code of the Skeletal Cell Atlas App, written in Python using the [Dash framework](https://plotly.com/dash/). The app is currently running at [skeletalcellatlas.org](https://skeletalcellatlas.org/).

You can grab your own copy of the dataset from the address above (as a loom file), put it in the `data` directory, and follow one of the following approaches (run with or without Docker) to install and run a local version of the app on your machine.

For more information on the dataset and the app, please refer to [this preprint](https://www.biorxiv.org/content/10.1101/2022.03.14.484345v1).

## Build and Run Container on Docker Host

A `docker-compose.yaml` is provided to simplify building and running the
container for local testing.

Run the following command to build the image:

```
docker-compose build
```

To run the application simply type:

```
docker-compose up
```

The app can be accessed at http://localhost:8050.

The files folder of the project is automatically mounted in the container
as data folder at `/app/data`.

### Run shell in app container

Following command will open a bash shell in the running app container:

```
docker-compose exec app bash
```

The shell will opened in the directory where the application is installed.

Following command will launch the app container with an interactive bash shell:

```
docker-compose run --service-ports app bash
```

The option `--service-ports` is needed to publish service ports specified
in the `docker-compose.yaml` file to the host computer.

## Configuration

Configuration of the app is done by passing environment variables to
the running container. Following environment variables are used:

- `DATA_PATH`: location of the data files (default: `/app/data`)
- `SERVER_PORT`: The port on which the app is exposed (default: 8050)
- `UPLOAD_PASSWORD`: Password for data upload

>>>
Note: If the app is launched directly in a shell (see next section), i.e.
not within a container, the environment variables can be set in a `.env`
file in the root folder of the project.
>>>

## Run app without Docker

Install all requirements:

```bash
$ pip install -r requirements.txt
```

Create `.env` file defining the environment variable `DATA_PATH` to point
to the location of the data files, e.g.:

```bash
$ echo DATA_PATH=files > .env
```

Launch the app like this:

```bash
$ python -m app.main
```

The app can be accessed at http://localhost:8050.
