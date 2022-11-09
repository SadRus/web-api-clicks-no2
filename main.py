import requests
import os
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(url, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    payload = {
        'long_url': url
    }
    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks',
                             headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['id']


def count_clicks(parsed_url, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{parsed_url}/clicks/summary',
        headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_link_shorten(parsed_url, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{parsed_url}',
        headers=headers)
    return response.ok


def main():
    load_dotenv()
    token = os.environ['BITLY_TOKEN']
    url = input()
    parsed_url = urlparse(url).netloc + urlparse(url).path
    try:
        if is_link_shorten(parsed_url, token):
            print('Count clicks', count_clicks(parsed_url, token))
        else:
            print('Bitlink', shorten_link(url, token))
    except requests.exceptions.HTTPError as error:
        exit(f"Can't get data from server: {error}")


if __name__ == '__main__':
    main()
