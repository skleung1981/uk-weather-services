from fastapi import FastAPI

from uk_weather_services.api.locations import location_handler

app = FastAPI()

@app.get("/v1/locations")
def get_locations():
    return location_handler.get_locations()


@app.get("/v1/version")
def read_root():

    return {
        'Version': "1.0.0"
    }


