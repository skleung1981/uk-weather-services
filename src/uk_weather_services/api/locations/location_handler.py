
# Please change it if it is necessary
DEFAULT_LOCATION = 'London'

# Please add locations for your action
SUPPORT_LOCATIONS = {
    'London':     {'latitude': 51.5074, 'longitude': -0.1278},
    'Birmingham': {'latitude': 52.4862, 'longitude': -1.8904},
    'Manchester': {'latitude': 53.4808, 'longitude': -2.2426},
    'Leeds':      {'latitude': 53.8008, 'longitude': -1.5491},
    'Glasgow':    {'latitude': 55.8642, 'longitude': -4.2518},
    'Edinburgh':  {'latitude': 55.9533, 'longitude': -3.1883},
    'Liverpool':  {'latitude': 53.4084, 'longitude': -2.9916},
    'Bristol':    {'latitude': 51.4545, 'longitude': -2.5879},
    'Sheffield':  {'latitude': 53.3811, 'longitude': -1.4701},
    'Cardiff':    {'latitude': 51.4816, 'longitude': -3.1791},
    'Belfast':    {'latitude': 54.5973, 'longitude': -5.9301},
    'Newcastle':  {'latitude': 54.9783, 'longitude': -1.6178},
}

_LOCATIONS_BY_KEY = {name.casefold(): coords for name, coords in SUPPORT_LOCATIONS.items()}

def get_location(location: str | None = None) -> dict:

    if not location or not location.strip():
        raise ValueError('Location is required')

    key = location.strip().casefold()
    try:
        return _LOCATIONS_BY_KEY[key]
    except KeyError:
        raise ValueError(f'Location not supported: {location!r}') from None

def get_locations() -> dict:
    return SUPPORT_LOCATIONS

def get_default_location() -> dict | None:
    return SUPPORT_LOCATIONS.get(DEFAULT_LOCATION, None)