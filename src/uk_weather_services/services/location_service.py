from uk_weather_services.api.locations import location_handler


def get_locations() -> dict:
    return location_handler.get_locations()