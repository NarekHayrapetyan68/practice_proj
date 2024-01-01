def upload_pizza_image(instance, filename):
    return f"pizzas/{instance.pizza_name}/{filename}"


def upload_user_images(instance, filename):
    return f"users/{instance.user.username}/{filename}"




