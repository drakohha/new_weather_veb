from django.shortcuts import render, HttpResponseRedirect
import requests
from .models import City
from .forms import CityForm


def index(request):
    appid = '563419681fd350c5d50f3dff8a5fa416'
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=" + appid
    cities = City.objects.all()

    if (request.method == 'POST'):
        form = CityForm(request.POST)
        form.save()
    form = CityForm

    all_cities = []

    for city in cities:
        res = requests.get(url.format(city)).json()
        sity_info = {
            'city': city.name,
            'temp': res["main"]["temp"],
            'icon': res["weather"][0]["icon"]
        }
        all_cities.append(sity_info)
    context = {
        'all_info': all_cities,
        'form': form
    }

    return render(request, 'weather/index.html', context)


def delete(request):
    City.objects.all().delete()
    return HttpResponseRedirect("/")
