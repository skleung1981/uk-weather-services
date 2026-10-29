import os
from typing import Annotated

from fastapi import FastAPI
from fastapi.params import Path, Query

from uk_weather_services.services import (
    location_service,
    spot_data_service,
    warning_service,
)

app = FastAPI()

sport_data_api_key = os.getenv('MET_OFFICE_SITE_SPECIFIC_GLOBAL_SPOT_DATA_API_KEY', '')
warning_api_key = os.getenv('MET_OFFICE_WARNING_API_KEY', '')

@app.get('/v1/spot-data/{query_type}')
def get_spot_data(
    query_type: Annotated[str, Path()],
    location: Annotated[str, Query()] = 'London',
):
    return spot_data_service.get_global_spot_data(sport_data_api_key, query_type, location)

@app.get('/v1/locations')
def get_locations() -> dict:
    return location_service.get_locations()


@app.get('/v1/warnings')
def get_warnings() -> dict:
    return warning_service.get_warnings(warning_api_key)


@app.get('/v1/version')
def read_root():

    return {
        'Version': '1.0.0'
    }


