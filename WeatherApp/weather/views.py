from django.shortcuts import render
import requests

def index(request):
    appid= '563419681fd350c5d50f3dff8a5fa416'
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=" + appid
    city='Minsk'
    res= requests.get(url.format(city))
    print(res.text)
    return render(request,'weather/index.html')