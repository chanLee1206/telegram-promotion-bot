import requests

# Specify the URL for the NFT
url = "https://api.blockberry.one/sui/v1/collections/0xd3ac4fb6dc7657884ae6c851df1d350cf1859b2d41287b5dd37150eecde29c11::my_minter::Nft"

# Set the headers, including the API key
headers = {
    "accept": "*/*",
    "x-api-key": "MVPNEj1vnMdkHsYrZppVgcoqYbJWcH"  # Replace with your actual API key
}

# Make the GET request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Print the JSON response
    print(response.json())  # Use .json() to parse the response as JSON
else:
    # Print an error message
    print(f"Error: {response.status_code} - {response.text}")
