import requests

# url = "https://api.blockberry.one/sui/v1/coins/0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY"
url = "https://api.blockberry.one/sui/v1/coins/0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY/transactions?page=0&size=20&orderBy=DESC&sortBy=AGE"
# Set the headers, including the API key
headers = {
    "accept": "*/*",
    "x-api-key": "MVPNEj1vnMdkHsYrZppVgcoqYbJWcH"  # Replace with your actual API key
}

# Make the GET request
response = requests.post(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Print the JSON response
    print(response.json())  # Use .json() to parse the response as JSON
else:
    # Print an error message
    print(f"Error: {response.status_code} - {response.text}")
