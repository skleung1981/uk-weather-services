import requests

API_ENDPOINT = 'https://data.hub.api.metoffice.gov.uk/sitespecific/v0/{endpoint}'

DATA_SOURCE = 'BD1'
OPTIONAL_PARAMS = {'includeLocationName', 'excludeParameterMetadata'}

HOURLY = 'point/hourly'
THREE_HOURLY = 'point/three-hourly'
DAILY = 'point/daily'


def get_hourly_data(api_key:str, latitude:float, longitude:float, data_source: str = DATA_SOURCE, **kwargs) -> dict:
    return _get_data(api_key, HOURLY, latitude, longitude, data_source, **kwargs)

def get_three_hourly_data(api_key:str, latitude:float, longitude:float, data_source: str = DATA_SOURCE, **kwargs) -> dict:
    return _get_data(api_key, THREE_HOURLY, latitude, longitude, data_source, **kwargs)

def get_daily_data(api_key:str, latitude:float, longitude:float, data_source: str = DATA_SOURCE, **kwargs) -> dict:
    return _get_data(api_key, DAILY, latitude, longitude, data_source, **kwargs)

def _get_data(api_key:str, endpoint_type:str, latitude:float, longitude:float, data_source: str = DATA_SOURCE, **kwargs) -> dict:

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

    final_api_endpoint = API_ENDPOINT.format(endpoint=endpoint_type)

    response = requests.get(
        final_api_endpoint,
        headers={'apikey': api_key, 'accept': 'application/json'},
        params=params,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
