from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):
    if request.method == 'POST' and 'city' in request.POST:
        city = request.POST['city']
    else:
        city = ''

    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=4d5db3077aab4940a618b3a762e3be89'
    PARAMS = {'units': 'metric'}
    
    API_KEY = '' 
    SEARCH_ENGINE_ID = '' 

    image_url = ''  
    if API_KEY and SEARCH_ENGINE_ID:
        query = city + " 1920x1080"
        page = 1
        start = (page - 1) * 10 + 1
        searchType = 'image'
        city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

        try:
            image_data = requests.get(city_url).json()
            search_items = image_data.get("items")
            if search_items and len(search_items) > 1:
                image_url = search_items[1].get('link', '')
        except Exception as e:
            print("Image search failed:", e)

    try:
        data = requests.get(weather_url, params=PARAMS).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })
    
    except KeyError:
        messages.error(request, 'Entered data is not available to API')   
        day = datetime.date.today()
        return render(request, 'weatherapp/index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'indore',
            'exception_occurred': True,
            'image_url': image_url
        })
