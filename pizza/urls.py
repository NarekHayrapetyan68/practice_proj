from django.urls import path
from .views import pizza, about_us, burger, home, rest_detail,\
    pizza_detail, burger_detail, search, add_burger_to_restaurant, add_pizza_to_restaurant

urlpatterns = [
    path("burgers/", burger, name="burgers"),
    path("pizzas/", pizza, name="pizzas"),
    path("about-us/", about_us, name="about_us"),
    path("", home, name="home"),
    path("restaurants/<str:restaurant_name>", rest_detail, name="restaurants"),
    path("pizzas/<str:name>", pizza_detail, name="pizza_page"),
    path("burgers/<str:name>", burger_detail, name="burger_page"),
    path("search/", search, name="search_page"),
    path('restaurant/<str:restaurant_name>/add_burger/', add_burger_to_restaurant, name='add_burger_to_restaurant'),
    path('restaurant/<str:restaurant_name>/add_pizza/', add_pizza_to_restaurant, name='add_pizza_to_restaurant'),
]
