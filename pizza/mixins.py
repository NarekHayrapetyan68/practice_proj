from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect


def profile_decorator(func: callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]
        if request.user.pk != kwargs.get("pk"):
            messages.error(request, "Invalid attempt!")
            return redirect("pizzas")
        return func(*args, **kwargs)
    return wrapper


class OwnProFileMixin:

    @method_decorator(login_required)
    @method_decorator(profile_decorator)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
