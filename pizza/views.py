from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Pizza, Burger, Restaurant


def pizza(request):
    pizzas = Pizza.objects.all()
    paginator = Paginator(pizzas, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "pizza/all_pizza.html", {"pizzas": page_obj})

# def pizza_detail(request, pk: int):
#     pizza = get_object_or_404(Pizza, pk=pk)
#     return render(request, "pizza/all_pizza.html", {"pizza": pizza})


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
