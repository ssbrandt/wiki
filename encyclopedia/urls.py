from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.view_entry, name="entry"),
    path("results/", views.search_results, name="results"),
    path("random/", views.random_entry, name="random"),
    path("new/", views.new_entry, name="new"),
    path("edit/", views.edit_entry, name="edit")
]