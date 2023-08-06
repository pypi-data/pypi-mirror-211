import requests

from jwt_validate.config import settings


def generate_jwt():
    headers = {
        'x-api-key': '451a6926-7ce7-491f-abe6-656d699d4783',
    }

    response = requests.get(
        settings.VAL_REQUEST_URL_TOKEN,
        headers=headers,
    )
    result = {
        'token': response.json()['accessToken'],
        'status_code': response.status_code,
    }

    return result
