from django.urls import path
from .views import pizza, about_us, burger

urlpatterns = [
    path("burgers", burger, name="burgers"),
    path("", pizza, name="pizzas"),
    path("about-us/", about_us, name="about_us")
]
