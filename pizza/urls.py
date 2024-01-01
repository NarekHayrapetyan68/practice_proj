from django.urls import path

from .views.details import PizzaDetailView, BurgerDetailView, BurgerView, PizzaView,\
                      RestaurantDetailView, AboutUsView, HomeView, SearchView

from .views.views import PizzaUpdateView, BurgerUpdateView, BurgerDeleteView, PizzaDeleteView, AddBurgerView,\
    AddPizzaView, AddRestaurantView


urlpatterns = [
    path("burgers/", BurgerView.as_view(), name="burgers"),
    path("pizzas/", PizzaView.as_view(), name="pizzas"),
    path("about-us/", AboutUsView.as_view(), name="about_us"),
    path("", HomeView.as_view(), name="home"),
    path("restaurants/<str:restaurant_name>", RestaurantDetailView.as_view(), name="restaurants"),
    path("pizzas/<str:name>", PizzaDetailView.as_view(), name="pizza_page"),
    path("burgers/<str:name>", BurgerDetailView.as_view(), name="burger_page"),
    path("search/", SearchView.as_view(), name="search_page"),
    path("restaurant/<str:restaurant_name>/add_burger/", AddBurgerView.as_view(), name="add_burger_to_restaurant"),
    path("restaurant/<str:restaurant_name>/add_pizza/", AddPizzaView.as_view(), name="add_pizza_to_restaurant"),
    path("pizzas/<str:name>/update/", PizzaUpdateView.as_view(), name="update_pizza"),
    path("burgers/<str:name>/update/", BurgerUpdateView.as_view(), name="update_burger"),
    path("pizzas/<str:name>/delete/", PizzaDeleteView.as_view(), name="delete_pizza"),
    path("burgers/<str:name>/delete/", BurgerDeleteView.as_view(), name="delete_burger"),
    path("add_restaurant/", AddRestaurantView.as_view(), name="add_restaurants"),

]
