import requests
import json


def get_access_token():
    email_id = ''
    api_key = ''
    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        'email': email_id,
        'password': api_key,
    }

    response = requests.post(
        'https://developers.cjdropshipping.com/api2.0/v1/authentication/getAccessToken',
        headers=headers,
        json=json_data,
    )
    content = json.loads(response.text)
    access_token = content['data']['accessToken']
    open("access_token.txt", "w").write(access_token)


try:
    access_token_ = open("access_token.txt", "r").read()
except:
    access_token_ = ''
if not access_token_:
    get_access_token()
