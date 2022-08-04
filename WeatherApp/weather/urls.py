from django.urls import path
from . import views
from .views import RegisterView, LoginWiev , UserView , Logout

urlpatterns = [

    path('', views.index),
    path('delete/',views.delete ,name="delete"),
    path('register', RegisterView.as_view()),
    path('login', LoginWiev.as_view()),
    path('user', UserView.as_view()),
    path('logout', Logout.as_view()),



]
