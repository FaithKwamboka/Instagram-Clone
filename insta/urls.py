from django.urls import path
from insta import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.Home, name="Home"),
    path('login', views.Login, name="Login"),
    path('register', views.Register, name="Register"),
]