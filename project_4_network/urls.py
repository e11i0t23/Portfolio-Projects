
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="project_4_network/index"),
    path("login", views.login_view, name="project_4_network/login"),
    path("logout", views.logout_view, name="project_4_network/logout"),
    path("register", views.register, name="project_4_network/register"),

    # Api Paths
    path("api/posts/<int:page>/", views.posts, kwargs={'user_id': None}, name="project_4_network/posts"),
    path("api/posts/<int:page>/following", views.posts, kwargs={'user_id': 'following'}, name="project_4_network/posts"),
    path("api/posts/<int:page>/user/<int:user_id>", views.posts, name="project_4_network/posts"),
    path("api/post/", views.editpost, kwargs={'id': None}, name="project_4_network/editpost"),
    path("api/post/<int:id>", views.editpost, name="project_4_network/editpost"),
    path("api/user/<int:id>", views.user, name="project_4_network/user")
    
]
