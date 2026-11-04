
from uk_weather_services.api.locations import coordinate_helper, location_handler
from uk_weather_services.api.site_specific import global_spot_data_handler


def get_global_spot_data(api_key: str,
                         period: str,
                         location: str | None = None,
                         *,
                         latitude: float | None = None,
                         longitude: float | None = None) -> dict:
    if not period:
        raise ValueError('Endpoint period is required')
    if (latitude is None) != (longitude is None):
        raise ValueError('latitude and longitude must be given together')

    has_location = location is not None
    has_coords = latitude is not None

    if has_location == has_coords:
        raise ValueError('Provide either location, or both latitude and longitude')

    if has_location:
        location_details = location_handler.get_location(location)
        latitude = location_details['latitude']
        longitude = location_details['longitude']
    else:
        latitude = coordinate_helper.validate_coord('latitude', latitude, -90, 90)
        longitude = coordinate_helper.validate_coord('longitude', longitude, -180, 180)

    return global_spot_data_handler.get_global_spot_data(api_key, period, latitude, longitude)