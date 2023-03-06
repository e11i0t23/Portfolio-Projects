from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="project_0_search/index"),
    path("image", views.image, name="project_0_search/image"),
    path("advanced", views.advanced, name="project_0_search/advanced")
]
