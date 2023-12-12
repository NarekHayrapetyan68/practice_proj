from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Pizza, Burger, Restaurant
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from .forms import SearchForm, BurgerForm, PizzaForm


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

    paginator = Paginator(items_to_display, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'restaurant': restaurant,
        'items': page_obj,
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
    if name := request.GET.get("name"):
        form = SearchForm(request.GET)
        if request.GET.get("product_type") == "burger":
            product_table = Burger
            name_search = Q(name__icontains=name)
        else:
            product_table = Pizza
            name_search = Q(name__icontains=name)
        if form.is_valid():
            calories_until = form.cleaned_data.get("calories_until")
            result_product = product_table.objects.filter(
                name_search |
                (Q(rate__lte=form.cleaned_data.get("rate_until") or 0) & Q(
                    rate__gte=form.cleaned_data.get("rate_from") or 0)) |
                Q(calories__lte=calories_until if calories_until is not None else 0)
            )
    return render(request, "pizza/search.html", {"form": form,
                                                 "result_product": result_product})


def add_burger_to_restaurant(request, restaurant_name):
    restaurant = get_object_or_404(Restaurant, restaurant_name=restaurant_name)

    if request.method == "POST":
        form = BurgerForm(request.POST, request.FILES)
        if form.is_valid():
            burger = form.save()
            restaurant.burgers.add(burger)
            return redirect('restaurants', restaurant_name=restaurant_name)
    else:
        form = BurgerForm()

    return render(request, "pizza/add_burger.html", {"form": form, "restaurant": restaurant})


def add_pizza_to_restaurant(request,restaurant_name):
    restaurant = get_object_or_404(Restaurant, restaurant_name=restaurant_name)

    if request.method == "POST":
        form = PizzaForm(request.POST, request.FILES)
        if form.is_valid():
            pizza = form.save()
            restaurant.pizzas.add(pizza)
            return redirect('restaurants', restaurant_name=restaurant_name)
    else:
        form = PizzaForm()

    return render(request, "pizza/add_pizza.html", {"form": form, "restaurant": restaurant})


