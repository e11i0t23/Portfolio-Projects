from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home/index"),
    path("login/<str:ref>", views.login_view, name="login"),
    path("logout/<str:ref>", views.logout_view, name="logout"),
    path("register/<str:ref>", views.register, name="register"),
]