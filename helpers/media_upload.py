def upload_pizza_image(instance, filename):
    return f"pizzas/{instance.pizza_name}/{filename}"
