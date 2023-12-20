from django import forms
from django.forms import inlineformset_factory

from .models import Burger, Pizza, Restaurant

RATE_CHOICES = [(0, "---")] + [(rate, f"{rate}") for rate in range(1, 11)]
PRODUCT_TYPE_CHOICES = [("pizza", "pizza"), ("burger", "burger")]


class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["calories_until"].widget.attrs.update(
            {"class": "form-control search-slt"}
        )
        self.fields["name"].widget.attrs.update(
            {"class": "form-control search-slt", "placeholder": "Name"}
        )

    name = forms.CharField(max_length=100, label="Product Name", required=True)
    rate_from = forms.ChoiceField(
        choices=RATE_CHOICES,
        widget=forms.Select(
                            attrs={"class": "form-control search-slt"}
                            ), label="Rate From", required=False
    )
    rate_until = forms.ChoiceField(
        choices=RATE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control search-slt"},
                            ), label="Rate Until", required=False
    )
    calories_until = forms.FloatField(max_value=1000, min_value=1,
                                      label="Calories Until",
                                      required=False)
    product_type = forms.ChoiceField(choices=PRODUCT_TYPE_CHOICES,
                                     widget=forms.Select(attrs={"class": "form-control search-slt"}
                                                         ), required=False)


class BurgerForm(forms.ModelForm):
    class Meta:
        model = Burger
        fields = '__all__'


class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = '__all__'


class RestaurantForm(forms.ModelForm):
    # burgers = forms.ModelMultipleChoiceField(queryset=Burger.objects.all())
    # pizzas = forms.ModelMultipleChoiceField(queryset=Pizza.objects.all())

    class Meta:
        model = Restaurant
        fields = '__all__'

