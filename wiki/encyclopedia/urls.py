from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>/" , views.get_entry , name="article"),
    path("wiki/create-page" , views.create_page , name="create-page"),
    path("wiki/add-page" , views.add_page , name="add-page"),
    path("random", views.get_random , name="random"),
    path("search" , views.search_entry , name="search"),
    path("save" , views.save_entry , name="save"),
    path("edit-page/<str:title>", views.edit_page , name="edit-page")
]
