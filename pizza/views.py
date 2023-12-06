from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Pizza, Burger, Restaurant
from django.views.decorators.csrf import csrf_protect


def pizza(request):
    pizzas = Pizza.objects.all()
    paginator = Paginator(pizzas, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "pizza/all_pizza.html", {"pizzas": page_obj})

@csrf_protect
def rest_detail(request, restaurant_name):
    restaurant = get_object_or_404(Restaurant, restaurant_name=restaurant_name)
    items_to_display = restaurant.pizzas.all()
    page_to_display = 'pizza_page'

    if request.method == 'POST':
        item_type = request.POST.get('item_type')
        if item_type == 'burger':
            items_to_display = restaurant.burgers.all()
            page_to_display = 'burger_page'
    context = {
        'restaurant': restaurant,
        'items': items_to_display,
        'page': page_to_display
    }

    return render(request, "pizza/restaurant_page.html", context)


def burger(request):
    burgers = Burger.objects.all()
    paginator = Paginator(burgers, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "pizza/all_burger.html", {"burgers": page_obj})


def about_us(request):
    return render(request, "pizza/about_us.html")


def home(request):
    restaurants = Restaurant.objects.all().order_by('pk')
    paginator = Paginator(restaurants, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "pizza/home.html", {"restaurants": page_obj})


def pizza_detail(request, pizza_name):
    pizzas = get_object_or_404(Pizza, pizza_name=pizza_name)
    return render(request, 'pizza/pizza_detail.html', {'pizzas': pizzas})


def burger_detail(request, burger_name):
    burgers = get_object_or_404(Burger, burger_name=burger_name)
    return render(request, 'pizza/burger_detail.html', {'burgers': burgers})
