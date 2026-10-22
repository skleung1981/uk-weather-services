# UK Weather Services

## Introduction
It is a small python project that used to get the UK weather data from Met Office.

### Notice
This original repository is not stored in the GitHub, it is stored in private repo in Forgejo but synchronized it to my GitHub account

## How to build

To build the python package
```
python -m build
```

To build the docker image 

```
docker compose -f docker-compose-local-dev.yaml build
```

## How to use

There are two ways to use it

1. Use it as a Python library
2. Run it as an API server using FastAPI via port 10080
```
docker compose -f docker-compose-local-dev.yaml up -d
```

### Configuration

For a standalone library, you need the following
- API keys from Met office for corresponding data feed and put it as a parameter

For an API server, you need the following
- API keys from Met office for corresponding data feed and put it as an environment variable. Please see local docker file and compose file.

