import requests

def fetch_coin_details(coin_type):
    url = f"https://api.blockberry.one/sui/v1/coins/{coin_type}"
    headers = {
        "accept": "*/*",
        "x-api-key": "MVPNEj1vnMdkHsYrZppVgcoqYbJWcH"
    }

    # Make the GET request
    response = requests.get(url, headers=headers)
    
    # Check response status and return the result if successful
    if response.status_code == 200:
        coin_details = response.json()
        return coin_details        
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
def main():
    # Example usage
    coin_type = "0xd976fda9a9786cda1a36dee360013d775a5e5f206f8e20f84fad3385e99eeb2d::aaa::AAA"
    # coin_type = "0xdeeb7a4662eec9f2f3def03fb937a663dddaa2e215b8078a284d026b7946c270::deep::DEEP"
    # coin_type = "0xe0fbaffa16409259e431b3e1ff97bf6129641945b42e5e735c99aeda73a595ac::suiyan::SUIYAN"
    # coin_type = "0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY"
    coin_info = fetch_coin_details(coin_type)
    print(coin_info)

if __name__ == "__main__":
    main()