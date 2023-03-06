from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="project_1_wiki/index"),
    path("random/", views.random, name="project_1_wiki/random"),
    path("wiki/<str:entry>/", views.wikientry, name="project_1_wiki/wikientry"),
    path("edit", views.edit, name="project_1_wiki/edit")
]
