import requests

url = "https://skyscanner80.p.rapidapi.com/api/v1/hotels/search"

querystring = {"entityId":"27539520","checkin":"2024-05-06","checkout":"2024-05-07","rooms":"1","adults":"1","resultsPerPage":"15","page":"1","currency":"USD","market":"EU","locale":"en-EU"}

headers = {
	"X-RapidAPI-Key": "403db7ccc1mshd98038a30cf2acfp1f34a1jsn38e6b0efbff7",
	"X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())