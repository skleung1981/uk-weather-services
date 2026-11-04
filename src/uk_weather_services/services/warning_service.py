from uk_weather_services.api.warnings import warnings_data_handler


def get_warnings(api_key: str) -> dict:
    return {
        'warnings' : warnings_data_handler.get_feed(api_key)
    }

def get_issued_warnings(api_key: str, uuid: str) -> dict:
    return warnings_data_handler.get_issued_warning(api_key, uuid)

def get_updated_warnings(api_key: str, uuid: str) -> dict:
    return warnings_data_handler.get_updated_warning(api_key, uuid)