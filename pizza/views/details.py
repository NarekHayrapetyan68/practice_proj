from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from pizza.models import Pizza, Burger, Restaurant
from django.db.models import Q
from pizza.forms import SearchForm, BurgerForm, PizzaForm, RestaurantForm
from django.views.generic import ListView, DetailView, TemplateView


class RestaurantDetailView(ListView):
    model = Restaurant
    template_name = 'pizza/restaurant_page.html'
    context_object_name = 'items'
    paginate_by = 3

    def get_queryset(self):
        restaurant_name = self.kwargs.get('restaurant_name')
        restaurant = get_object_or_404(Restaurant, restaurant_name=restaurant_name)
        burgers = self.request.GET.get("burgers")

        if burgers == "True":
            return restaurant.burgers.all()
        else:
            return restaurant.pizzas.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant_name = self.kwargs.get('restaurant_name')
        context['restaurant'] = get_object_or_404(Restaurant, restaurant_name=restaurant_name)
        return context


class PizzaDetailView(DetailView):
    model = Pizza
    template_name = 'pizza/pizza_detail.html'
    context_object_name = 'pizzas'
    pk_url_kwarg = 'name'

    def get_object(self, queryset=None):
        name = self.kwargs.get('name')
        return get_object_or_404(Pizza, name=name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pizza = self.object
        similar_pizzas = Pizza.objects.exclude(name=pizza.name)

        price = pizza.price
        calories = pizza.calories

        similar_pizzas = similar_pizzas.filter(
            (Q(price__lte=price + 5) & Q(price__gte=price - 5)) |
            (Q(calories__gte=calories - 5) & Q(calories__lte=calories + 5))
        )

        context['similar'] = similar_pizzas
        return context


class BurgerDetailView(DetailView):
    model = Burger
    template_name = "pizza/burger_detail.html"
    context_object_name = 'burgers'
    pk_url_kwarg = 'name'

    def get_object(self, queryset=None):
        name = self.kwargs.get('name')
        return get_object_or_404(Burger, name=name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        burger = self.object
        similar_burger = Burger.objects.exclude(name=burger.name)

        price = burger.price
        calories = burger.calories

        similar_burger = similar_burger.filter(
            (Q(price__lte=price + 5) & Q(price__gte=price - 5)) |
            (Q(calories__gte=calories - 5) & Q(calories__lte=calories + 5))
        )

        context['similar'] = similar_burger
        return context


class SearchView(ListView):
    template_name = 'pizza/search.html'
    context_object_name = 'result_product'
    form_class = SearchForm

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        queryset = []

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
                    queryset = Burger.objects.filter(base_query)
                elif product_type == "pizza":
                    queryset = Pizza.objects.filter(base_query)
            else:
                base_query &= Q(rate__gte=rate_from) if rate_from is not None else Q()
                base_query &= Q(rate__lte=rate_until) if rate_until is not None else Q()
                base_query &= Q(calories__lte=calories_until) if calories_until is not None else Q()

                queryset = Pizza.objects.filter(base_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        return context


class AboutUsView(TemplateView):
    template_name = "pizza/about_us.html"


class HomeView(ListView):
    model = Restaurant
    template_name = "pizza/home.html"
    context_object_name = 'restaurants'
    paginate_by = 4
    ordering = ['pk']

    def get_queryset(self):
        return Restaurant.objects.all().order_by('pk').prefetch_related('burgers', 'pizzas')


class BurgerView(ListView):
    model = Burger
    template_name = "pizza/all_burger.html"
    context_object_name = 'burgers'
    paginate_by = 2

    def get_queryset(self):
        return Burger.objects.all().order_by('pk')


class PizzaView(ListView):
    model = Pizza
    template_name = "pizza/all_pizza.html"
    context_object_name = 'pizzas'
    paginate_by = 2

    def get_queryset(self):
        return Pizza.objects.all().order_by('pk')
