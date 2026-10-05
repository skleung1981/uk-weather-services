import datetime
import uuid
import xml.etree.ElementTree as Et

import requests

API_ENDPOINT = 'https://data.hub.api.metoffice.gov.uk/nswws/v1.1/{endpoint}'

FEED = 'objects/feed'
ISSUED = 'objects/issued/{uuid}'
UPDATED = 'objects/updated/{uuid}'

def get_feed(api_key:str) -> list[dict]:
    ns = {'atom': 'http://www.w3.org/2005/Atom'}

    xml_str = _get_data(api_key, FEED)

    returned_dict = []
    root = Et.fromstring(xml_str)
    for entry in root.findall("atom:entry", ns):
        warning = {}
        entry_id: str | None = entry.find("atom:id", ns).text
        entry_id = str(uuid.UUID(entry_id)) if entry_id else None

        updated: str | None = entry.find("atom:updated", ns).text
        updated = (
            datetime.datetime.strptime(updated, '%Y-%m-%dT%H:%M:%SZ')
            .replace(tzinfo=datetime.UTC)
            .isoformat()
            if updated else None
        )

        link = entry.find("atom:link", ns).get("href") if entry.find("atom:link", ns) is not None else None

        warning.update({
            'entry_id' : entry_id,
            'last_updated' : updated,
            'summary': entry.find("atom:summary", ns).text,
            'link': link,
        })
        print(warning)
        returned_dict.append(warning)

    return returned_dict

def _get_data(api_key:str, endpoint_type:str, uuid:str|None = None) -> str:

    final_api_endpoint = API_ENDPOINT.format(endpoint=endpoint_type)

    response = requests.get(
        final_api_endpoint,
        headers={'apikey': api_key, 'accept': 'application/atom+xml'},
        timeout=10,
    )
    response.raise_for_status()
    return response.text
