import requests

# Specify the URL for the NFT
url = "https://api.blockberry.one/sui/v1/collections/0xcc2650b0d0b949e9cf4da71c22377fcbb78d71ce9cf0fed3e724ed3e2dc57813%3A%3Aboredapesuiclub_collection%3A%3ABoredApeSuiClub"

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
