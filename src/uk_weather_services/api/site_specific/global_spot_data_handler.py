import requests

API_ENDPOINT = 'https://data.hub.api.metoffice.gov.uk/sitespecific/v0/{endpoint}'

DATA_SOURCE = 'BD1'
OPTIONAL_PARAMS = {'includeLocationName', 'excludeParameterMetadata'}

HOURLY = 'point/hourly'
THREE_HOURLY = 'point/three-hourly'
DAILY = 'point/daily'

LATITUDE_MIN, LATITUDE_MAX = -85.0, 85.0
LONGITUDE_MIN, LONGITUDE_MAX = -180.0, 180.0

def _get_hourly_data(api_key: str, latitude: float, longitude: float, data_source: str = DATA_SOURCE, **kwargs) -> dict:
    return _get_data(api_key, HOURLY, latitude, longitude, data_source, **kwargs)

def _get_three_hourly_data(api_key: str, latitude: float, longitude: float, data_source: str = DATA_SOURCE, **kwargs) -> dict:
    return _get_data(api_key, THREE_HOURLY, latitude, longitude, data_source, **kwargs)

def _get_daily_data(api_key: str, latitude: float, longitude: float, data_source: str = DATA_SOURCE, **kwargs) -> dict:
    return _get_data(api_key, DAILY, latitude, longitude, data_source, **kwargs)

def _get_data(api_key: str, endpoint_type: str, latitude: float, longitude: float, data_source: str = DATA_SOURCE, **kwargs) -> dict:

    params = {
        'latitude': latitude,
        'longitude': longitude,
        'dataSource': data_source,
    }

    for key, value in kwargs.items():
        if key not in OPTIONAL_PARAMS:
            raise TypeError(f"Unexpected parameter: {key}")
        if isinstance(value, bool):
            value = str(value).lower()   # True -> "true"
        params[key] = value

    url = API_ENDPOINT.format(endpoint=endpoint_type)

    response = requests.get(
        url,
        headers={'apikey': api_key, 'accept': 'application/json'},
        params=params,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


endpoints = {
    'hourly' : _get_hourly_data,
    'three-hourly': _get_three_hourly_data,
    'daily': _get_daily_data
}


def get_global_spot_data(api_key: str, endpoint_type: str, latitude: float, longitude: float, **kwargs) -> dict:

    if not api_key or not api_key.strip():
        raise ValueError('API key is required')

    if not LATITUDE_MIN <= latitude <= LATITUDE_MAX:
        raise ValueError(f'Latitude must be between {LATITUDE_MIN} and {LATITUDE_MAX}, got {latitude}')
    if not LONGITUDE_MIN <= longitude <= LONGITUDE_MAX:
        raise ValueError(f'Longitude must be between {LONGITUDE_MIN} and {LONGITUDE_MAX}, got {longitude}')

    try:
        handler = endpoints[endpoint_type]
    except KeyError:
        raise ValueError(f'Unsupported endpoint type: {endpoint_type!r}') from None

    return handler(api_key, latitude, longitude, **kwargs)