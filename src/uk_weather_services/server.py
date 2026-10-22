
from fastapi import FastAPI

from uk_weather_services.services import location_service

app = FastAPI()

@app.get('/v1/spot-data/hourly')
def get_spot_data():
    pass

@app.get('/v1/locations')
def get_locations():
    return location_service.get_locations()


@app.get('/v1/version')
def read_root():

    return {
        'Version': '1.0.0'
    }


