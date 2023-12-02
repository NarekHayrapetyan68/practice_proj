from django.db import models



def upload_pizza_image(instance, filename):
    return f"{instance.pizza_name}/{filename}"


def upload_burger_image(instance, filename):
    return f"{instance.burger_name}/{filename}"


def upload_restaurant_image(instance, filename):
    return f"{instance.restaurant_name}/{filename}"


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    image = models.ImageField(upload_to=restaurant_name, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.restaurant_name


class Pizza(models.Model):
    pizza_name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    rate = models.FloatField(default=0)
    prepare_time = models.FloatField(null=True, blank=True)
    calories = models.FloatField(blank=True)
    price = models.FloatField()
    image = models.ImageField(upload_to=upload_pizza_image, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name='pizza')

    def __str__(self):
        return self.pizza_name


class Burger(models.Model):
    burger_name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    rate = models.FloatField(default=0)
    prepare_time = models.FloatField(null=True, blank=True)
    calories = models.FloatField(blank=True)
    price = models.FloatField()
    image = models.ImageField(upload_to=upload_burger_image, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name='burger')

    def __str__(self):
        return self.burger_name

