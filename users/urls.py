from django.urls import path
from .views import SignUpView, Login, UserLogoutView, UserProfileView, UserUpdateView

# from django.contrib.auth.views import LoginView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/<int:pk>/", UserProfileView.as_view(), name="profile"),
    path("edit-profile/<int:pk>/", UserUpdateView.as_view(), name="edit_profile"),

]
