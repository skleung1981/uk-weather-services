
from uk_weather_services.api.locations import location_handler


def test_locations():
    assert len(location_handler.get_locations().items()) > 0

def test_get_default_location():
    assert location_handler.get_default_location() is not None