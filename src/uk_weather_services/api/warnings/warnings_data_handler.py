import datetime
import uuid
import xml.etree.ElementTree as Et
from typing import Any, Literal

import requests

API_ENDPOINT = 'https://data.hub.api.metoffice.gov.uk/nswws/v1.1/{endpoint}'

FEED = 'objects/feed'
ISSUED = 'objects/issued/{entry_uuid}'
UPDATED = 'objects/updated/{entry_uuid}'

NAMESPACE = {'atom': 'http://www.w3.org/2005/Atom'}

Format = Literal['xml', 'json']
_ACCEPT_HEADERS: dict[str, str] = {
    'xml': 'application/atom+xml',
    'json': 'application/json',
}

def get_feed(api_key: str) -> list[dict]:

    _validate_input(api_key, FEED)

    xml_str = _get_data(api_key, FEED)

    returned_dict = []
    root = Et.fromstring(xml_str)
    for entry in root.findall("atom:entry", NAMESPACE):
        warning = {}
        entry_id: str | None = entry.find("atom:id", NAMESPACE).text
        entry_id = str(uuid.UUID(entry_id)) if entry_id else None

        updated: str | None = entry.find("atom:updated", NAMESPACE).text
        updated = (
            datetime.datetime.strptime(updated, '%Y-%m-%dT%H:%M:%SZ')
            .replace(tzinfo=datetime.UTC)
            .isoformat()
            if updated else None
        )

        link = entry.find("atom:link", NAMESPACE).get("href") if entry.find("atom:link", NAMESPACE) is not None else None

        warning.update({
            'entry_id' : entry_id,
            'last_updated' : updated,
            'summary': entry.find("atom:summary", NAMESPACE).text,
            'link': link,
        })

        returned_dict.append(warning)
    print(f'Number of warnings: {len(returned_dict)}')
    return returned_dict


def get_issued_warning(api_key: str, entry_id: str) -> dict:
    _validate_input(api_key, ISSUED)
    return _get_data(api_key, ISSUED, entry_id, fmt='json')


def get_updated_warning(api_key: str, entry_id: str) -> dict:
    _validate_input(api_key, UPDATED)
    return _get_data(api_key, UPDATED, entry_id, fmt='json')


def _validate_input(api_key: str, endpoint_type: str, entry_id: str | None = None) -> None:
    if not api_key or not api_key.strip():
        raise ValueError('API key is required')
    if not endpoint_type or not endpoint_type.strip():
        raise ValueError('Endpoint type is required')
    if entry_id is not None:
        try:
            uuid.UUID(entry_id)
        except (ValueError, TypeError, AttributeError):
            raise ValueError(f'entry_id must be a valid UUID, got {entry_id!r}') from None


def _get_data(api_key: str, endpoint_type: str, entry_id: str | None = None, *, fmt: Format = 'xml') -> Any:

    try:
        accept = _ACCEPT_HEADERS[fmt]
    except KeyError:
        raise ValueError(f'Unsupported format: {fmt!r}') from None

    url = API_ENDPOINT.format(endpoint=endpoint_type)
    if entry_id:
        url = url.format(entry_uuid=entry_id)

    response = requests.get(
        url,
        headers={'apikey': api_key, 'accept': accept},
        timeout=10,
    )
    response.raise_for_status()
    content_type = response.headers.get('Content-Type', '')
    if 'json' in content_type:
        return response.json()
    return response.text
