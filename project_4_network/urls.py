
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="project_4_network/index"),

    # Api Paths
    path("api/posts/<int:page>/", views.posts, kwargs={'user_id': None}, name="project_4_network/posts"),
    path("api/posts/<int:page>/following", views.posts, kwargs={'user_id': 'following'}, name="project_4_network/posts"),
    path("api/posts/<int:page>/user/<int:user_id>", views.posts, name="project_4_network/posts"),
    path("api/post/", views.editpost, kwargs={'id': None}, name="project_4_network/editpost"),
    path("api/post/<int:id>", views.editpost, name="project_4_network/editpost"),
    path("api/user/<int:id>", views.user, name="project_4_network/user")
    
]
