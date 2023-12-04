from django.urls import path
from .views import pizza, about_us, burger, home, rest_detail

urlpatterns = [
    path("burgers/", burger, name="burgers"),
    path("pizzas/", pizza, name="pizzas"),
    path("about-us/", about_us, name="about_us"),
    path("", home, name="home"),
    path("restaurants/", rest_detail, name="restaurants")
]
