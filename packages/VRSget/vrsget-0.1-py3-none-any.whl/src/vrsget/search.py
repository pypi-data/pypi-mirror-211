import requests

def getStations(station):
    url = 'https://ekap-web.vrs.de/index.php'
    params = {
        'eID': 'tx_vrsinfo_ass2_objects',
        'srv': 'web',
        'ta': 'vrs',
        't': 's',
        'c': '25',
        'f': 'f',
        'q': station
    }
    headers = {
        'Sec-Ch-Ua': '"Chromium";v="113", "Not-A.Brand";v="24"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Origin': 'https://www.vrs.de',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.vrs.de/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    response = requests.get(url, params=params, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        data = response.json()
        stations = data["stops"]
        return(stations)
    else:
        return("Request failed with status code:", response.status_code)

stations = getStations("a")
for station in stations:
    print(f"neue station: {station}")