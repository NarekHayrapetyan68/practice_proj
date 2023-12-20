from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from pizza.models import Pizza, Burger, Restaurant
from django.db.models import Q
from pizza.forms import SearchForm, BurgerForm, PizzaForm, RestaurantForm


def rest_detail(request, restaurant_name):
    restaurant = get_object_or_404(Restaurant, restaurant_name=restaurant_name)
    items_to_display = restaurant.pizzas.all()
    if burgers := request.GET.get("burgers"):
        if burgers == "True":
            items_to_display = restaurant.burgers.all()

    paginator = Paginator(items_to_display, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'restaurant': restaurant,
        'items': page_obj,
    }

    return render(request, "pizza/restaurant_page.html", context)


def pizza_detail(request, name):
    pizzas = get_object_or_404(Pizza, name=name)
    similar_pizzas = Pizza.objects.exclude(name=name)
    price = pizzas.price
    calories = pizzas.calories
    similar_pizzas = similar_pizzas.filter((Q(price__lte=price+5) & Q(price__gte=price-5)) |
                                           (Q(calories__gte=calories-5) & Q(calories__lte=calories+5)))

    return render(request, 'pizza/pizza_detail.html', {'pizzas': pizzas, 'similar': similar_pizzas})


def burger_detail(request, name):
    burgers = get_object_or_404(Burger, name=name)
    similar_burgers = Burger.objects.exclude(name=name)
    price = burgers.price
    calories = burgers.calories
    similar_burgers = similar_burgers.filter((Q(price__in=range(int(price)-5, int(price)+5)) |
                                              Q(calories__in=range(int(calories)-50, int(calories)+100))))

    return render(request, 'pizza/burger_detail.html', {'burgers': burgers , 'similar': similar_burgers})


def search(request):
    form = SearchForm()
    result_product = []

    if request.method == 'GET':
        form = SearchForm(request.GET)

        if form.is_valid():
            name = form.cleaned_data.get("name")
            product_type = form.cleaned_data.get("product_type")
            rate_from = form.cleaned_data.get("rate_from")
            rate_until = form.cleaned_data.get("rate_until")
            calories_until = form.cleaned_data.get("calories_until")

            base_query = Q()

            if name:
                base_query &= Q(name__icontains=name)

            if product_type:
                if product_type == "burger":
                    result_product = Burger.objects.filter(base_query)
                elif product_type == "pizza":
                    result_product = Pizza.objects.filter(base_query)
            else:
                base_query &= Q(rate__gte=rate_from) if rate_from is not None else Q()
                base_query &= Q(rate__lte=rate_until) if rate_until is not None else Q()
                base_query &= Q(calories__lte=calories_until) if calories_until is not None else Q()

                result_product = Pizza.objects.filter(base_query)

    return render(request, "pizza/search.html", {"form": form, "result_product": result_product})


def about_us(request):
    return render(request, "pizza/about_us.html")


def home(request):
    restaurants = Restaurant.objects.all().order_by('pk').prefetch_related('burgers', 'pizzas')
    paginator = Paginator(restaurants, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "pizza/home.html", {"restaurants": page_obj})


def burger(request):
    burgers = Burger.objects.all()
    paginator = Paginator(burgers, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "pizza/all_burger.html", {"burgers": page_obj})


def pizza(request):
    pizzas = Pizza.objects.all()
    paginator = Paginator(pizzas, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "pizza/all_pizza.html", {"pizzas": page_obj})
