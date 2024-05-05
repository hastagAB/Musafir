import requests

def get_geo_id(city_name: str):
    url = "https://tripadvisor-com1.p.rapidapi.com/auto-complete"

    querystring = {"query": city_name}

    headers = {
        "X-RapidAPI-Key": "3df56689e1mshb6954452a2cec15p1e3346jsna689ad4acefd",
        "X-RapidAPI-Host": "tripadvisor-com1.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()
        
        if "data" in data:
            for item in data["data"]:
                if "geoId" in item:
                    return int(item["geoId"])
        
        return None
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

