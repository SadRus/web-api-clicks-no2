import json
import requests
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()


def shorten_link(token, url):
    if 'http:' in url:
        url = url.replace('http', 'https')
    response = requests.get(url)
    response.raise_for_status()
    headers = {
        'Authorization': f'Bearer {token}'
    }
    data = {
        'long_url': url
    }
    data = json.dumps(data)

    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks',
                             headers=headers, data=data)
    response.raise_for_status()
    bitlink = json.loads(response.text)['id']
    return bitlink


def count_clicks(token, bitlink):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {
        'unit': 'day',
        'units': '-1'
    }
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary',
        headers=headers, params=params)
    response.raise_for_status()
    return json.loads(response.text)['total_clicks']


def is_link_shorten(url):
    if 'bit.ly' in urlparse(url).path:
        return True
    return False


def main():
    token = os.environ['TOKEN']
    url = input()
    try:
        if is_link_shorten(url):
            print('Count clicks', count_clicks(token, url))
        else:
            print('Bitlink', shorten_link(token, url))
    except requests.exceptions.ConnectionError as error:
        exit(f"Can't get data from server: {error}")


if __name__ == '__main__':
    main()
