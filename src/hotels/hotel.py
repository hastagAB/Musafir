import requests
import csv
from attraction.geoID import get_geo_id

def search_hotels(geo_id, checkin_date, checkout_date):
    url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchHotels"
    querystring = {
        "geoId": geo_id,
        "checkIn": checkin_date,
        "checkOut": checkout_date,
        "pageNumber": "1",
        "currencyCode": "USD"
    }
    headers = {
        "X-RapidAPI-Key": "266d9aaa66mshe070908b4466057p1b5147jsn035de0fa6ca1",
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_top_5_hotels(data):
    top_hotels = []
    if data and 'data' in data:
        hotels = data['data']['data']
        for hotel in hotels[:5]:
            title = hotel.get('title')
            rating = hotel.get('bubbleRating', {}).get('rating')
            provider = hotel.get('provider')
            price = hotel.get('priceForDisplay')
            hotel_info = {
                "title": title,
                "rating": rating,
                "provider": provider,
                "price": price
            }
            top_hotels.append(hotel_info)
    return top_hotels

# Define parameters
def Hotels(city, checkin_date, checkout_date):
    geo_id = get_geo_id(city)
    stays_info = search_hotels(geo_id, checkin_date, checkout_date)
    top_hotels = get_top_5_hotels(stays_info)
    return top_hotels
