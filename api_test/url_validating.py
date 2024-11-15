import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urlparse

import requests

def check_url_availability(url):
    try:
        response = requests.get(url)
        print (response)
        if response.status_code == 200:
            print("URL is available and reachable.")
            return {'availability': True}
        else:
            print("URL is not reachable. Status code:", response.status_code)
            return {'availability': False}
            
    except requests.RequestException as e:
        # Log the error if the request fails
        print("Error occurred:", str(e))
        return {'availability': False, 'error': str(e)}

async def main():
    url = "https://movepump.com/token/0x92d6bab4e7495e6fb92a70809d652df1b4f61941c44619aea7a8763fcc0f5045::suilion"
    result = check_url_availability(url)
    print(result)


if __name__ == "__main__":
    asyncio.run(main()) 