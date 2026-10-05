
# Please change it if it is necessary
DEFAULT_LOCATION = 'London'

# Please add locations for your action
SUPPORT_LOCATIONS = {
    'London': { 'latitude': 51.5074, 'longitude': -0.1278 }
}

def get_locations() -> dict:
    return SUPPORT_LOCATIONS

def get_default_location() -> dict | None:
    return SUPPORT_LOCATIONS.get(DEFAULT_LOCATION, None)