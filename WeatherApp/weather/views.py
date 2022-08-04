from django.shortcuts import render, HttpResponseRedirect
import requests
from .models import City
from .forms import CityForm
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt , datetime


class RegisterView(APIView):
    def post(self, request):
        serializer= UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginWiev(APIView):
    def post(self,request):
        email=request.data['email']
        password=request.data['password']

        user= User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed("Пользователь не найден")

        payload={
            'id': user.id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=300),
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret',algorithm='HS256').decode('utf-8')
        response= Response()
        response.set_cookie(key='jwt', value=token , httponly=True)
        response.data={
            'jwt':token
        }
        return response


class UserView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')


        if not token:
            raise AuthenticationFailed("Не прошедший проверку подлинности")
        try:
            payload =jwt.decode(token,'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Не прошедший проверку подлинности")

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


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


class Logout(APIView):
    def post(self,request):
        response=Response()
        response.delete_cookie('jwt')
        response.data={
            'messege':" Успешно"
        }
        return  response