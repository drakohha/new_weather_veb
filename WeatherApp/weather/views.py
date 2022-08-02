from django.shortcuts import render
import requests

def index(request):
    appid= '563419681fd350c5d50f3dff8a5fa416'
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=" + appid
    city='Minsk'
    res = requests.get(url.format(city)).json()

    sity_info={
        'city': city,
        'temp': res["main"]["temp"],
        'icon': res["weather"][0]["icon"]
    }
    context={
        'info': sity_info
    }
    return render(request,'weather/index.html',context)