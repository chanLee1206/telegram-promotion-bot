import requests

# nft Collection Info
# url = "https://api.blockberry.one/sui/v1/collections/0xcc2650b0d0b949e9cf4da71c22377fcbb78d71ce9cf0fed3e724ed3e2dc57813%3A%3Aboredapesuiclub_collection%3A%3ABoredApeSuiClub"

# token transaction Info https://api.blockberry.one/sui/v1/coins/{coinType}/transactions
url = "https://api.blockberry.one/sui/v1/coins/0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY/transactions?page=0&size=3&orderBy=DESC&sortBy=AGE"

# https://api.blockberry.one/sui/v1/coins/{coinType}/holders
# url = "https://api.blockberry.one/sui/v1/coins/0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY/holders?page=0&size=20&orderBy=DESC&sortBy=AMOUNT"

# Set the headers, including the API key
headers = {
    "accept": "*/*",
    "x-api-key": "MVPNEj1vnMdkHsYrZppVgcoqYbJWcH"  # Replace with your actual API key
}

# Make the GET request
# response = requests.get(url, headers=headers)
response = requests.post(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Print the JSON response
    print(response.json())  # Use .json() to parse the response as JSON
else:
    # Print an error message
    print(f"Error: {response.status_code} - {response.text}")
