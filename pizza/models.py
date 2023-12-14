from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse



def upload_pizza_image(instance, filename):
    return f"{instance.name}/{filename}"


def upload_burger_image(instance, filename):
    return f"{instance.name}/{filename}"


def upload_restaurant_image(instance, filename):
    return f"{instance.restaurant_name}/{filename}"


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    image = models.ImageField(upload_to=restaurant_name, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    burgers = models.ManyToManyField('Burger', related_name='burger', blank=True)
    pizzas = models.ManyToManyField('Pizza', related_name='pizza', blank=True)

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"
        ordering = ["restaurant_name"]

    def __str__(self):
        return self.restaurant_name


class Pizza(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    rate = models.FloatField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    prepare_time = models.FloatField(null=True, blank=True)
    calories = models.FloatField(blank=True)
    price = models.FloatField()
    image = models.ImageField(upload_to=upload_pizza_image, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("pizza_page", kwargs={'name': self.name})

    def __str__(self):
        return self.name


class Burger(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    rate = models.FloatField(default=0, null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
    prepare_time = models.FloatField(null=True, blank=True)
    calories = models.FloatField(blank=True,null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to=upload_burger_image, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("burger_page", kwargs={'name': self.name})

    def __str__(self):
        return self.name