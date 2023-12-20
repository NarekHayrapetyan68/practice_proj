from django.forms import formset_factory
from django.shortcuts import render, get_object_or_404, redirect
from pizza.models import Pizza, Burger, Restaurant
from pizza.forms import SearchForm, BurgerForm, PizzaForm, RestaurantForm
from django.contrib import messages


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


def update_pizza(request, name: str):
    pizza = get_object_or_404(Pizza, name=name)
    form = PizzaForm(instance=pizza)
    if request.method == "POST":
        form = PizzaForm(request.POST, request.FILES, instance=pizza)
        if form.is_valid():
            form.save()
            messages.info(request, f"{pizza.name} was updated successfully!")
            return redirect("pizzas")
    return render(request, "pizza/pizza_update.html", {"form": form})


def update_burger(request, name: str):
    burger = get_object_or_404(Burger, name=name)
    form = BurgerForm(instance=burger)
    if request.method == "POST":
        form = BurgerForm(request.POST, request.FILES, instance=burger)
        if form.is_valid():
            form.save()
            messages.info(request, f"{burger.name} was updated successfully!")
            return redirect("burgers")
    return render(request, "pizza/burger_update.html", {"form": form})


def delete_pizza(request, name: str):
    pizza = get_object_or_404(Pizza, name=name)
    if request.method == 'POST':
        pizza.delete()
        messages.error(request, f"{pizza.name} was deleted!")
        return redirect('pizzas')
    return render(request, "pizza/delete_pizza.html", {"pizza": pizza})


def delete_burger(request, name: str):
    burger = get_object_or_404(Burger, name=name)
    if request.method == 'POST':
        burger.delete()
        messages.error(request, f"{burger.name} was deleted!")
        return redirect('burgers')
    return render(request, "pizza/delete_burger.html", {"burger": burger})


def add_restaurants(request):
    BurgerFormSet = formset_factory(BurgerForm, extra=1, can_delete=True)
    PizzaFormSet = formset_factory(PizzaForm, extra=1, can_delete=True)
    restaurants = Restaurant.objects.all()

    if request.method == 'POST':
        restaurant_form = RestaurantForm(request.POST, request.FILES)
        burger_formset = BurgerFormSet(request.POST, prefix='burgers')
        pizza_formset = PizzaFormSet(request.POST, prefix='pizzas')

        if (
                restaurant_form.is_valid()
                and burger_formset.is_valid()
                and pizza_formset.is_valid()
                and burger_formset.total_form_count() >= 2
                and pizza_formset.total_form_count() >= 2
        ):
            restaurant = restaurant_form.save()

            for form in burger_formset:
                if form.is_valid() and not form.cleaned_data.get('DELETE', False):
                    burger = form.save(commit=False)
                    burger.save()
                    restaurant.burgers.add(burger)

            for form in pizza_formset:
                if form.is_valid() and not form.cleaned_data.get('DELETE', False):
                    pizza = form.save(commit=False)
                    pizza.save()
                    restaurant.pizzas.add(pizza)

            restaurant.save()

            return redirect('home')

    else:
        restaurant_form = RestaurantForm()
        burger_formset = BurgerFormSet(prefix='burgers')
        pizza_formset = PizzaFormSet(prefix='pizzas')

    return render(
        request,
        'pizza/add_rest.html',
        {'form': restaurant_form, 'burger_formset': burger_formset, 'pizza_formset': pizza_formset})