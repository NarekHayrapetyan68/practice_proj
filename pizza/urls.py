from django.urls import path
from .views import pizza, about_us, burger, home, rest_detail, pizza_detail, burger_detail

urlpatterns = [
    path("burgers/", burger, name="burgers"),
    path("pizzas/", pizza, name="pizzas"),
    path("about-us/", about_us, name="about_us"),
    path("", home, name="home"),
    path("restaurants/<str:restaurant_name>", rest_detail, name="restaurants"),
    path("pizzas/<str:name>", pizza_detail, name="pizza_page"),
    path("burgers/<str:name>", burger_detail, name="burger_page")
]
