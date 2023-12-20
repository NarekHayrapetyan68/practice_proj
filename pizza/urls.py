from django.urls import path

from .views.details import pizza_detail, burger_detail, burger, pizza,\
                      rest_detail, about_us, search, home

from .views.views import update_pizza, update_burger, delete_burger, delete_pizza, add_burger_to_restaurant,\
    add_pizza_to_restaurant, add_restaurants


urlpatterns = [
    path("burgers/", burger, name="burgers"),
    path("pizzas/", pizza, name="pizzas"),
    path("about-us/", about_us, name="about_us"),
    path("", home, name="home"),
    path("restaurants/<str:restaurant_name>", rest_detail, name="restaurants"),
    path("pizzas/<str:name>", pizza_detail, name="pizza_page"),
    path("burgers/<str:name>", burger_detail, name="burger_page"),
    path("search/", search, name="search_page"),
    path("restaurant/<str:restaurant_name>/add_burger/", add_burger_to_restaurant, name="add_burger_to_restaurant"),
    path("restaurant/<str:restaurant_name>/add_pizza/", add_pizza_to_restaurant, name="add_pizza_to_restaurant"),
    path("pizzas/<str:name>/update/", update_pizza, name="update_pizza"),
    path("burgers/<str:name>/update/", update_burger, name="update_burger"),
    path("pizzas/<str:name>/delete/", delete_pizza, name="delete_pizza"),
    path("burgers/<str:name>/delete/", delete_burger, name="delete_burger"),
    path("add_restaurant/", add_restaurants, name="add_restaurants"),

]
