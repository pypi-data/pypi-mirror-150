import requests
from requests.exceptions import HTTPError

#TODO Do status code validation and raise errors
def http_get(url: str):
    try:
        response = requests.get(url, headers={'content-type':'application/json'})
        # Raise HTTPError according to status code
        response.raise_for_status()
    except HTTPError as http_err:
        raise HTTPError(http_err)
    except Exception as err:
        raise Exception(err)
    else:
        return response
