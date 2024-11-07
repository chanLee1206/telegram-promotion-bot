import json

# Data to be stored in JSON format
data = {
    'name': 'Ancy Peosi',
    'symbol': 'ANCY',
    'decimals': 6,
    'logo': 'https://api.movepump.com/uploads/266_4adcb9f78e.jpeg',
    'price': '0.0000016337461960862802510591',
    'priceChangePercentage24H': '163.27',
    'totalSupply': '10000000000',
    'holders': 337,
    'marketCap': '16337.4620',
    'packageID': '0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508',
    'coinType': '0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY',
    'creator': '0x465539fb4566a4638c02fd6206abdae0cddc25d4da926fc8bdbbf9d74f59b6be',
    'createdTime': 1729469613846,
    'birdeyeLink': 'https://birdeye.so/token/0x197aece533dbee36b7698cead0403dfecafa421b3aaa55a15314062a5f640508::ancy::ANCY?chain=sui'
}

# Write data to JSON file
with open('token_info.json', 'w') as f:
    json.dump(data, f, indent=4)

# Load and print JSON data from the file
with open('token_info.json', 'r') as f:
    loaded_data = json.load(f)
    print(loaded_data)
