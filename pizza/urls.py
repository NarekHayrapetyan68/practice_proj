from django.urls import path
from pizza.views import pizza, about_us

urlpatterns = [
    path("", pizza, name="pizzas"),
    path("about-us/", about_us, name="about_us")
]
