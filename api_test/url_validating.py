import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Define async function to check URL availability and extract meta data if URL contains 'movepump'
async def check_url_and_extract_meta(url):
    try:
        # Asynchronously send a GET request to the URL
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # Check if the status code is OK
                if response.status == 200:
                    print("URL is available and reachable.")

                    # Extract coinType and symbol from the URL
                    parsed_url = urlparse(url)
                    path_parts = parsed_url.path.split('/')
                    coinType = path_parts[-1]
                    symbol = coinType.split("::")[-1]

                    if 'movepump' in url:
                        # Only extract meta data if the URL contains "movepump"
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')

                        # Extract content from the <meta> tag
                        twitter_title_meta = soup.find('meta', attrs={'name': 'twitter:title'})

                        # Parse the content of the twitter:title meta tag
                        if twitter_title_meta and 'content' in twitter_title_meta.attrs:
                            title_content = twitter_title_meta['content']
                            # Split the title content to get the name and launchPad
                            name, launchPad = map(str.strip, title_content.split('|'))

                            # Prepare dictionary with extracted data
                            token_info = {
                                'launchPad': launchPad,
                                'name': name,
                                'symbol': symbol,
                                'coinType': coinType
                            }

                            return {'availability': True, 'metaData': token_info}
                        else:
                            return {'availability': True, 'metaData': None}
                    else:
                        # If the URL does not contain "movepump", return availability status only
                        return {'availability': True, 'metaData': None}

                else:
                    return {'availability': False, 'metaData': None}

    except Exception as e:
        return {'availability': False, 'metaData': None, 'error': str(e)}

# Example usage of the async function
async def main():
    url = "https://movepump.com/token/0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY"
    result = await check_url_and_extract_meta(url)
    print(result)

    url2 = "https://example.com/token/0x1234567890abcdef::xyz::XYZ"
    result2 = await check_url_and_extract_meta(url2)
    print(result2)

# Run the async main function
asyncio.run(main())
