import os

from uk_weather_services.api.locations import location_handler
from uk_weather_services.api.site_specific import global_spot_data_handler


def get_hourly_data(api_key, latitude, longitude):
    api_key = os.getenv('MET_OFFICE_SITE_SPECIFIC_GLOBAL_SPOT_DATA_API_KEY')
    location = location_handler.get_locations().get('London')
    if api_key is not None and location is not None:
        latitude = location.get('latitude')
        longitude = location.get('longitude')
        return global_spot_data_handler.get_hourly_data(api_key, latitude, longitude)
    else:
        return {'error': 'API key not provided'}