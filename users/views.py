from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy,reverse
from .mixins import OwnProFileMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegistrationForm, ProfileForm
from django.contrib.auth.models import User


class SignUpView(CreateView):
    template_name = 'users/user_registration.html'
    success_url = reverse_lazy('home')
    form_class = RegistrationForm
    success_message = "Your profile was created successfully"

    def form_valid(self, form):
        response = super().form_valid(form)

        self.object.profile.phone_number = form.cleaned_data["phone_number"]
        self.object.profile.country = form.cleaned_data["country"]
        self.object.profile.image = form.cleaned_data["image"]
        self.object.profile.goal = form.cleaned_data["goal"]
        self.object.profile.save()
        messages.success(self.request, "User Created Successfully")
        return response


class Login(LoginView):
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    pass


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "auth/profile.html"


class UserUpdateView(OwnProFileMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "auth/edit_profile.html"

    def get_initial(self):
        profile = self.object.profile
        return {
            "phone_number": profile.phone_number,
            "country": profile.country,
            "image": profile.image,
        }

    def get_success_url(self):
        messages.success(self.request, "User updated successfully!")
        return reverse("profile", kwargs={"pk": self.object.pk})




