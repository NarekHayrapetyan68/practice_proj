from django.forms import formset_factory
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from pizza.models import Pizza, Burger, Restaurant
from pizza.forms import SearchForm, BurgerForm, PizzaForm, RestaurantForm
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


class AddBurgerView(LoginRequiredMixin, CreateView):
    model = Burger
    template_name = "pizza/add_burger.html"
    form_class = BurgerForm

    def get_object(self, queryset=None):
        name = self.kwargs.get('name')
        return get_object_or_404(Burger, name=name)

    def get_success_url(self):
        messages.success(self.request, "Burger created Successfully!")
        return reverse("home")


class AddPizzaView(LoginRequiredMixin, CreateView):
    model = Pizza
    template_name = "pizza/add_pizza.html"
    form_class = PizzaForm

    def get_object(self, queryset=None):
        name = self.kwargs.get('name')
        return get_object_or_404(Pizza, name=name)

    def get_success_url(self):
        messages.success(self.request, "Pizza created Successfully!")
        return reverse("home")


class PizzaUpdateView(LoginRequiredMixin, UpdateView):
    model = Pizza
    template_name = 'pizza/pizza_update.html'
    form_class = PizzaForm
    context_object_name = 'pizza'

    def get_object(self, queryset=None):
        name = self.kwargs.get('name')
        return get_object_or_404(Pizza, name=name)

    def get_success_url(self):
        messages.info(self.request, f"{self.object.name} was updated successfully!")
        return reverse_lazy('pizzas')


class BurgerUpdateView(LoginRequiredMixin, UpdateView):
    model = Burger
    template_name = 'pizza/burger_update.html'
    form_class = BurgerForm
    context_object_name = 'burger'

    def get_object(self, queryset=None):
        name = self.kwargs.get('name')
        return get_object_or_404(Burger, name=name)

    def get_success_url(self):
        messages.info(self.request, f"{self.object.name} was updated successfully!")
        return reverse_lazy('burgers')


class PizzaDeleteView(LoginRequiredMixin, DeleteView):
    model = Pizza
    template_name = 'pizza/delete_pizza.html'
    context_object_name = 'pizza'
    success_url = reverse_lazy('pizzas')

    def get_object(self, queryset=None):
        name = self.kwargs.get('name')
        return get_object_or_404(Pizza, name=name)

    def form_valid(self, form):
        messages.error(self.request, f"{self.object.name} was deleted!")
        return super().form_valid(form)


class BurgerDeleteView(LoginRequiredMixin, DeleteView):
    model = Burger
    template_name = 'pizza/delete_burger.html'
    context_object_name = 'burger'
    success_url = reverse_lazy('burgers')

    def get_object(self, queryset=None):
        name = self.kwargs.get('name')
        return get_object_or_404(Burger, name=name)

    def form_valid(self, form):
        messages.error(self.request, f"{self.object.name} was deleted!")
        return super().form_valid(form)


# def add_restaurants(request):
#     BurgerFormSet = formset_factory(BurgerForm, extra=1, can_delete=True)
#     PizzaFormSet = formset_factory(PizzaForm, extra=1, can_delete=True)
#     restaurants = Restaurant.objects.all()
#
#     if request.method == 'POST':
#         restaurant_form = RestaurantForm(request.POST, request.FILES)
#         burger_formset = BurgerFormSet(request.POST, request.FILES, prefix='burgers')
#         pizza_formset = PizzaFormSet(request.POST, request.FILES, prefix='pizzas')
#
#         if (
#                 restaurant_form.is_valid()
#                 and burger_formset.is_valid()
#                 and pizza_formset.is_valid()
#                 and burger_formset.total_form_count() >= 2
#                 and pizza_formset.total_form_count() >= 2
#         ):
#             restaurant = restaurant_form.save()
#
#             for form in burger_formset:
#                 if form.is_valid() and not form.cleaned_data.get('DELETE', False):
#                     burger = form.save(commit=False)
#                     burger.save()
#                     restaurant.burgers.add(burger)
#
#             for form in pizza_formset:
#                 if form.is_valid() and not form.cleaned_data.get('DELETE', False):
#                     pizza = form.save(commit=False)
#                     pizza.save()
#                     restaurant.pizzas.add(pizza)
#
#             restaurant.save()
#
#             return redirect('home')
#
#     else:
#         restaurant_form = RestaurantForm()
#         burger_formset = BurgerFormSet(prefix='burgers')
#         pizza_formset = PizzaFormSet(prefix='pizzas')
#
#     return render(
#         request,
#         'pizza/add_rest.html',
#         {'form': restaurant_form, 'burger_formset': burger_formset, 'pizza_formset': pizza_formset})
class AddRestaurantView(LoginRequiredMixin, CreateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = 'pizza/add_rest.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        BurgerFormSet = formset_factory(BurgerForm, extra=1, can_delete=True)
        PizzaFormSet = formset_factory(PizzaForm, extra=1, can_delete=True)
        context['burger_formset'] = BurgerFormSet(prefix='burgers')
        context['pizza_formset'] = PizzaFormSet(prefix='pizzas')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        burger_formset = context['burger_formset']
        pizza_formset = context['pizza_formset']

        if (
            burger_formset.is_valid()
            and pizza_formset.is_valid()
            and burger_formset.total_form_count() >= 2
            and pizza_formset.total_form_count() >= 2
        ):
            restaurant = form.save()

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

            return super().form_valid(form)

        return self.form_invalid(form)