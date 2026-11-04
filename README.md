# UK Weather Services

## Introduction

It is a small python project that is used to get the UK weather data from Met Office.

**This repo is originally from my local CI/CD environment using forgejo, this one you're viewing is the mirror version in GitHub.**

## Requirements
- Python version: 3.12+
- Libraries (Please refer to requirements.txt)
  - Requests
  - FastAPI

## How to build

To build the python package
```
python -m build
```

To build the docker image 

```
docker compose -f <docker compose file> build
```

## How to use

There are two ways to use it

1. Use it as a Python library
2. Run it as an API server using FastAPI via port 8080 (10080 for local-dev)
```
docker compose -f <docker compose file> up -d
```

### Configuration

For a standalone library, you need the following
- API keys from Met office for corresponding data feed and put it as a parameter

For an API server, you need the following
- API keys from Met office for corresponding data feed and put it as environment variables. Please see local docker file and compose file.
- if the API keys are stored in K8S as secret, please use the following commands
  ```
  kubectl create secret generic uk-weather-api-keys --namespace saturn-backend \
  --from-literal=spot-data-api-key=<> \
  --from-literal=warnings-api-key=<>
  ```

