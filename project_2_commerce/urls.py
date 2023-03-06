from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="project_2_commerce/index"),
    path("login", views.login_view, name="project_2_commerce/login"),
    path("logout", views.logout_view, name="project_2_commerce/logout"),
    path("register", views.register, name="project_2_commerce/register"),
    path("watching", views.watching, name="project_2_commerce/watching"),
    path("edit", views.edit, name="project_2_commerce/edit"),
    path("auction/<int:auc>", views.auctionpage, name="project_2_commerce/auctionpage")
]
