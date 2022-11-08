import requests
import os
#from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(url, headers):
    payload = {
        'long_url': url
    }
    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks',
                             headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['id']


def count_clicks(short_url, headers):
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{short_url}/clicks/summary',
        headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_link_shorten(url, headers):
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{url}',
                            headers=headers)
    if response.ok:
        return True
    return False


def main():
    token = os.environ['BITLY_TOKEN']
    headers = {
        'Authorization': f'Bearer {token}'
    }
    url = input()

    try:
        if is_link_shorten(url, headers):
            print('Count clicks', count_clicks(url, headers))
        else:
            print('Bitlink', shorten_link(url, headers))
    except requests.exceptions.HTTPError as error:
        exit(f"Can't get data from server: {error}")


if __name__ == '__main__':
    load_dotenv()
    main()
